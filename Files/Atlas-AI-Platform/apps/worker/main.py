"""Minimal background worker entry point.

The worker currently validates shared configuration/logging. It is a placeholder
host for later async jobs, analogous to starting an `IHostedService` process.
"""

import logging

from packages.core.config import get_settings
from packages.core.logging import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    # Keeping startup observable now prevents future queue workers from failing
    # silently when run outside the API process.
    logger.info("Starting Atlas worker", extra={"env": settings.env})


if __name__ == "__main__":
    main()
