"""Prompt test runner.

Prompt tests render a stored prompt version, execute it through the model
gateway, and evaluate simple expected-output checks. This gives prompt changes a
repeatable CI-style harness before activation.
"""

from __future__ import annotations

import json
import re
import time
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.core.errors import AppError
from packages.db.models.prompts import PromptTemplate, PromptTestCase, PromptVersion
from packages.model_gateway.client import ModelGateway
from packages.model_gateway.redaction import preview_text
from packages.model_gateway.types import ModelRequest, UseCase
from packages.prompts.contracts import (
    CheckResult,
    PromptTestOutcome,
    PromptTestResult,
    PromptTestSummary,
    ResolvedPromptVersion,
)
from packages.prompts.errors import PromptValidationError
from packages.prompts.records import version_spec_from_models
from packages.prompts.renderer import render_prompt
from packages.prompts.service import PromptService


class PromptTestRunner:
    """Runs persisted prompt test cases against a candidate version."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._service = PromptService(session)

    def run_prompt_tests(
        self,
        *,
        template_id: UUID,
        prompt_version_id: UUID,
        tenant_id: UUID | None = None,
        case_types: tuple[str, ...] = (),
        compare_to_active: bool = False,
    ) -> PromptTestSummary:
        template = self._service.get_template(template_id)
        version = self._service.get_version(
            template_id=template_id,
            version_id=prompt_version_id,
        )
        run_tenant_id = template.tenant_id or tenant_id
        if run_tenant_id is None:
            raise PromptValidationError(
                code="prompts.test_run_requires_tenant",
                message="A tenant_id is required to run tests for a global prompt.",
                details={"prompt_template_id": str(template.id)},
            )

        self._service.mark_testing(version=version, template=template)
        self._session.commit()

        baseline = (
            self._active_version(template_id)
            if compare_to_active and version.status != "active"
            else None
        )
        # Baseline comparison lets reviewers see regressions/fixes against the
        # currently active prompt, not just pass/fail for the candidate.
        cases = self._selected_cases(template_id=template_id, case_types=case_types)
        results: list[PromptTestResult] = []
        for test_case in cases:
            baseline_outcome: PromptTestOutcome | None = None
            if baseline is not None and baseline.id != version.id:
                baseline_outcome = self._run_single(
                    template=template,
                    version=baseline,
                    test_case=test_case,
                    tenant_id=run_tenant_id,
                ).outcome
            candidate_result = self._run_single(
                template=template,
                version=version,
                test_case=test_case,
                tenant_id=run_tenant_id,
            )
            results.append(
                PromptTestResult(
                    case_id=candidate_result.case_id,
                    case_name=candidate_result.case_name,
                    case_type=candidate_result.case_type,
                    outcome=candidate_result.outcome,
                    ai_run_id=candidate_result.ai_run_id,
                    output_preview=candidate_result.output_preview,
                    checks=candidate_result.checks,
                    duration_ms=candidate_result.duration_ms,
                    error_code=candidate_result.error_code,
                    error_message=candidate_result.error_message,
                    baseline_outcome=baseline_outcome,
                )
            )

        return _summary(version=version, baseline=baseline, results=tuple(results))

    def _active_version(self, template_id: UUID) -> PromptVersion | None:
        return self._session.scalars(
            select(PromptVersion).where(
                PromptVersion.prompt_template_id == template_id,
                PromptVersion.status == "active",
            )
        ).one_or_none()

    def _selected_cases(
        self,
        *,
        template_id: UUID,
        case_types: tuple[str, ...],
    ) -> list[PromptTestCase]:
        statement = select(PromptTestCase).where(
            PromptTestCase.prompt_template_id == template_id,
            PromptTestCase.status == "active",
        )
        if case_types:
            statement = statement.where(PromptTestCase.case_type.in_(case_types))
        return list(self._session.scalars(statement.order_by(PromptTestCase.created_at)).all())

    def _run_single(
        self,
        *,
        template: PromptTemplate,
        version: PromptVersion,
        test_case: PromptTestCase,
        tenant_id: UUID,
    ) -> PromptTestResult:
        started = time.perf_counter()
        try:
            # Render with `resolution="pinned"` so tests target the exact version
            # under review rather than whatever is currently active.
            rendered = render_prompt(
                ResolvedPromptVersion(
                    version=version_spec_from_models(version=version, template=template),
                    resolution="pinned",
                    cache_hit=False,
                ),
                test_case.input_json,
            )
            response = ModelGateway(self._session).chat(
                ModelRequest(
                    tenant_id=tenant_id,
                    use_case=cast(UseCase, template.use_case),
                    messages=rendered.messages,
                    prompt_version_id=rendered.prompt_version_id,
                    prompt_name=rendered.prompt_name,
                    prompt_version_number=rendered.prompt_version_number,
                    prompt_template_id=rendered.prompt_template_id,
                    prompt_resolution=rendered.resolution,
                    prompt_cache_hit=rendered.cache_hit,
                )
            )
            checks = _evaluate_checks(response.content or "", test_case.expected_output_json)
            outcome = _outcome_from_checks(checks, test_case.expected_output_json)
            if response.finish_reason == "length":
                checks = checks + (
                    CheckResult(
                        check="finish_reason",
                        result="failed",
                        argument="length",
                        message="Model response ended because of length.",
                    ),
                )
                outcome = "failed"
            return PromptTestResult(
                case_id=test_case.id,
                case_name=test_case.name,
                case_type=test_case.case_type,
                outcome=outcome,
                ai_run_id=response.ai_run_id,
                output_preview=preview_text(response.content or "", restricted=False),
                checks=checks,
                duration_ms=_elapsed_ms(started),
            )
        except AppError as exc:
            self._session.rollback()
            return PromptTestResult(
                case_id=test_case.id,
                case_name=test_case.name,
                case_type=test_case.case_type,
                outcome="error",
                checks=(),
                duration_ms=_elapsed_ms(started),
                error_code=exc.code,
                error_message=exc.message,
            )


def _evaluate_checks(
    content: str,
    expected_output_json: dict[str, Any] | None,
) -> tuple[CheckResult, ...]:
    """Evaluate declarative checks stored in `expected_output_json`."""
    checks = [CheckResult(check="completes", result="passed")]
    if expected_output_json is None:
        return tuple(checks)

    for expected in _as_list(expected_output_json.get("contains")):
        found = expected.lower() in content.lower()
        checks.append(
            CheckResult(
                check="contains",
                argument=expected,
                result="passed" if found else "failed",
            )
        )
    for forbidden in _as_list(expected_output_json.get("not_contains")):
        absent = forbidden.lower() not in content.lower()
        checks.append(
            CheckResult(
                check="not_contains",
                argument=forbidden,
                result="passed" if absent else "failed",
            )
        )
    for pattern in _as_list(expected_output_json.get("matches_regex")):
        matched = re.search(pattern, content) is not None
        checks.append(
            CheckResult(
                check="matches_regex",
                argument=pattern,
                result="passed" if matched else "failed",
            )
        )

    json_keys = _as_list(expected_output_json.get("json_keys_present"))
    if expected_output_json.get("is_json") or json_keys:
        try:
            parsed = json.loads(content)
            checks.append(CheckResult(check="is_json", result="passed"))
        except json.JSONDecodeError:
            parsed = None
            checks.append(CheckResult(check="is_json", result="failed"))
        if json_keys:
            if isinstance(parsed, dict):
                for key in json_keys:
                    checks.append(
                        CheckResult(
                            check="json_keys_present",
                            argument=key,
                            result="passed" if key in parsed else "failed",
                        )
                    )
            else:
                for key in json_keys:
                    checks.append(
                        CheckResult(
                            check="json_keys_present",
                            argument=key,
                            result="failed",
                        )
                    )

    max_output_tokens = expected_output_json.get("max_output_tokens")
    if max_output_tokens is not None:
        token_count = len(content.split())
        checks.append(
            CheckResult(
                check="max_output_tokens",
                argument=max_output_tokens,
                result="passed" if token_count <= int(max_output_tokens) else "failed",
            )
        )
    return tuple(checks)


def _outcome_from_checks(
    checks: tuple[CheckResult, ...],
    expected_output_json: dict[str, Any] | None,
) -> PromptTestOutcome:
    if any(check.result == "failed" for check in checks):
        return "failed"
    if expected_output_json is None:
        return "needs_review"
    return "passed"


def _summary(
    *,
    version: PromptVersion,
    baseline: PromptVersion | None,
    results: tuple[PromptTestResult, ...],
) -> PromptTestSummary:
    """Aggregate per-case results into a compact run summary."""
    passed = sum(result.outcome == "passed" for result in results)
    failed = sum(result.outcome == "failed" for result in results)
    error = sum(result.outcome == "error" for result in results)
    needs_review = sum(result.outcome == "needs_review" for result in results)
    regressions = sum(
        result.baseline_outcome == "passed" and result.outcome == "failed"
        for result in results
    )
    fixed = sum(
        result.baseline_outcome == "failed" and result.outcome == "passed"
        for result in results
    )
    return PromptTestSummary(
        prompt_version_id=version.id,
        version_number=version.version_number,
        baseline_version_id=baseline.id if baseline else None,
        baseline_version_number=baseline.version_number if baseline else None,
        provider_mode="mock",
        total=len(results),
        passed=passed,
        failed=failed,
        error=error,
        needs_review=needs_review,
        regressions=regressions,
        fixed=fixed,
        results=results,
    )


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _elapsed_ms(started: float) -> int:
    return max(0, int((time.perf_counter() - started) * 1000))
