# ============================================================================
# FILE: tests/deployment/test_local_deployment_files.py
#
# THINK OF THIS FILE AS: a packing-list check before the whole local system ships.
#
# WHAT THIS TESTS: that the files for a production-shaped local deployment still
# describe the expected services, browser console, monitoring setup, and
# end-to-end smoke-test path.
#
# Docker packages a program and its dependencies into an IMAGE. Running an image
# creates a CONTAINER: an isolated process with the same contents on every
# machine. Docker Compose reads docker-compose.yml and starts the group of
# containers that make one working SupportOps installation.
#
# WHERE THIS SITS IN THE LOCAL REQUEST FLOW:
#   docker-compose.yml starts Postgres and Redis
#     -> "migrate" creates the database schema
#       -> the API accepts tickets while the worker handles queued AI jobs
#         -> nginx serves apps/web/src/ to a browser
#           -> Prometheus collects API metrics and Grafana draws dashboards
#
# TESTING APPROACH: most checks are deliberately cheap text contracts. They make
# accidental deletion of a service, endpoint, port, or rollout step visible in
# the ordinary pytest suite without starting Docker. The Grafana dashboard is
# stronger in one respect: json.loads also proves that file remains valid JSON.
#
# HONEST LIMITATION: these tests do not parse the YAML files, build images, start
# containers, call an endpoint, or render a dashboard. A phrase can exist in the
# wrong YAML section and still satisfy a substring check. "docker compose
# config", the docker-build CI job in .github/workflows/ci.yml, and actually
# running scripts/deployment-smoke.ps1 provide progressively stronger evidence.
#
# A pytest FIXTURE is reusable setup supplied to a test. None is needed here:
# each test reads small committed files directly and does not create external
# services or shared state.
#
# WHO USES IT / WHAT LIVES HERE: docker-compose.yml wires the stack together;
# Dockerfile.web packages apps/web/src/index.html and app.js behind nginx;
# infra/prometheus/ and infra/grafana/ configure monitoring; the PowerShell smoke
# script exercises the same HTTP workflow a support agent uses.
# ============================================================================
import json
from pathlib import Path


# This checks the minimum service map and a few connections that make the map
# useful. "Production-like" means separate API, worker, web, data, and monitoring
# processes; it does not mean this laptop configuration is safe for production.
def test_compose_defines_local_production_like_services() -> None:
    # The YAML is read as text. YAML is a configuration format where indentation
    # defines nesting, so the leading spaces in later checks are significant.
    compose = Path("docker-compose.yml").read_text(encoding="utf-8")

    # One table-driven loop guards the eight essential services. Local-only Adminer
    # and Redis Commander tools also exist, but the application can operate without
    # those optional browser conveniences.
    for service_name in (
        # One-shot schema setup, followed by the two Python programs and web server.
        "migrate",
        "api",
        "worker",
        "web",
        # Durable ticket data and the queue carrying background job identifiers.
        "postgres",
        "redis",
        # Metric collection and the dashboard that displays the collected history.
        "prometheus",
        "grafana",
    ):
        # Two spaces plus a colon resembles a service key under "services:". This can
        # still match text in the wrong place, which is why Compose parsing also runs in CI.
        assert f"  {service_name}:" in compose

    # The API and worker must wait for the one-shot migration container to finish
    # successfully; merely starting at the same time risks querying tables that do
    # not exist yet.
    assert "condition: service_completed_successfully" in compose
    # CORS means Cross-Origin Resource Sharing: the browser's rule for which web
    # addresses may call the API. Both common spellings of the local host are needed.
    assert "CORS_ORIGINS: http://127.0.0.1:3000,http://localhost:3000" in compose
    # Compose port strings use "host:container". These expose the console on 3000,
    # Prometheus on 9090, and Grafana on 3001 while retaining their internal ports.
    assert '"3000:80"' in compose
    assert '"9090:9090"' in compose
    assert '"3001:3000"' in compose


# The browser console has three layers: Dockerfile.web builds its image, nginx
# serves index.html, and app.js calls the API. This test keeps all three present.
def test_web_image_and_static_console_are_present() -> None:
    dockerfile = Path("Dockerfile.web").read_text(encoding="utf-8")
    index = Path("apps/web/src/index.html").read_text(encoding="utf-8")
    script = Path("apps/web/src/app.js").read_text(encoding="utf-8")

    # nginx is the small web server in the final image; Alpine is its compact Linux
    # base. Pinning the expected tag makes an unnoticed base-image change visible.
    assert "nginx:1.27-alpine" in dockerfile
    # "Copilot Console" is a simple identity marker that catches an empty, replaced,
    # or mistakenly copied HTML entry page.
    assert "Copilot Console" in index
    # These are the API capabilities the console must expose from end to end:
    # liveness/readiness, policies, ticket intake, two analysis paths, and metrics.
    for endpoint in (
        "/health",
        "/ready",
        "/policies",
        "/tickets",
        # The synchronous route waits for AI; the queued route returns a run to poll.
        "/ai-analysis",
        "/analyze",
        # Human-review outcomes and model spending are the pilot's key measurements.
        "/metrics/reviews",
        "/metrics/costs",
    ):
        # Presence does not prove the JavaScript uses the correct HTTP method or handles
        # errors. Browser or end-to-end tests would be needed for those behaviours.
        assert endpoint in script


# "Provisioning" means configuring a tool from committed files at startup instead
# of relying on someone to repeat setup clicks. That makes monitoring repeatable.
def test_prometheus_and_grafana_are_provisioned() -> None:
    # Prometheus periodically "scrapes", or fetches, a metrics endpoint. Grafana then
    # reads those stored measurements through its configured Prometheus data source.
    prometheus = Path("infra/prometheus/prometheus.yml").read_text(encoding="utf-8")
    datasource = Path("infra/grafana/provisioning/datasources/prometheus.yml").read_text(
        encoding="utf-8"
    )
    dashboard_provider = Path(
        "infra/grafana/provisioning/dashboards/dashboards.yml"
    ).read_text(encoding="utf-8")
    # Unlike the YAML files above, the dashboard is parsed. Invalid JSON therefore
    # fails immediately instead of being treated as arbitrary text.
    dashboard = json.loads(
        Path("infra/grafana/dashboards/supportops-overview.json").read_text(encoding="utf-8")
    )

    # Prometheus must call the runtime-metrics route on the API service's internal
    # Compose address, not localhost inside the Prometheus container.
    assert "metrics_path: /metrics/runtime" in prometheus
    assert "api:8765" in prometheus
    # Grafana must reach Prometheus over the same Compose network and know where its
    # automatically mounted dashboards live.
    assert "url: http://prometheus:9090" in datasource
    assert "path: /var/lib/grafana/dashboards" in dashboard_provider
    # A stable title helps operators recognize that the expected dashboard loaded.
    assert dashboard["title"] == "SupportOps Local Overview"
    # Grafana panels contain targets, and each target contains a Prometheus query in
    # "expr". The nested loop searches every target and any requires at least one
    # query that graphs the model-cost counter.
    assert any(
        # get supplies an empty default for optional fields so unrelated panel shapes do
        # not cause a KeyError while the search continues.
        "model_cost_usd_total" in target.get("expr", "")
        for panel in dashboard["panels"]
        for target in panel.get("targets", [])
    )


# A SMOKE TEST is a short, broad check that the main system path works after
# deployment. It is named after checking whether a newly powered machine smokes:
# it catches obvious integration failures, not every subtle defect.
def test_deployment_smoke_script_exercises_full_ticket_workflow() -> None:
    script = Path("scripts/deployment-smoke.ps1").read_text(encoding="utf-8")

    # The expected strings trace one complete human-in-the-loop story:
    # seed demo identities -> add policy -> create ticket -> queue and poll analysis
    # -> fetch recommendation -> review it -> confirm review and cost metrics.
    for expected in (
        "python -m supportops_api.seed",
        "/policies",
        "/tickets",
        "/analyze",
        "/analysis",
        "/recommendations",
        "/reviews",
        "/metrics/reviews",
        "/metrics/costs",
    ):
        # This only checks that the steps remain named in the script. It does not run
        # PowerShell or prove a deployed API answers them successfully.
        assert expected in script
