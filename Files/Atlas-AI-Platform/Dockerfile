# Multi-stage build. The builder holds the compilers and build metadata; the
# runtime stage gets only the installed packages, which keeps the shipped image
# smaller and removes build tooling from the attack surface.
FROM python:3.11-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

# Copy the dependency manifest first. Docker caches this layer, so a source-only
# change does not trigger a full dependency reinstall.
COPY pyproject.toml README.md ./
COPY apps ./apps
COPY packages ./packages

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install .


FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

# Run as a non-root user. A container process that does not need root should
# never have it.
RUN useradd --create-home --uid 10001 atlas

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=atlas:atlas alembic.ini ./
COPY --chown=atlas:atlas apps ./apps
COPY --chown=atlas:atlas packages ./packages

USER atlas

EXPOSE 8000

# The readiness endpoint already checks PostgreSQL and Redis, so the container
# healthcheck reuses it rather than inventing a second definition of "healthy".
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/api/v1/health/live', timeout=3).status == 200 else 1)"

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
