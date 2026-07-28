# ============================================================================
# FILE: apps/api/supportops_api/settings.py
#
# THINK OF THIS FILE AS: the app's settings panel.
#
# Every value that might need to differ between your laptop, the test server,
# and the real production server lives here in one place — database address,
# AI model name, price per token, and so on. Nothing else in the codebase
# should hard-code these values; they all come from here.
#
# HOW THE VALUES GET FILLED IN:
#   This uses "pydantic-settings", a library that automatically looks for each
#   setting in two places, in this order:
#     1. An environment variable of the same name, in CAPITALS.
#        e.g. the `database_url` field below is filled from DATABASE_URL.
#     2. A file named `.env` sitting in the project folder (same NAME=value
#        format). Handy for local development.
#   If neither exists, the default written below is used.
#
#   That is why docker-compose.yml has long `environment:` lists — those are
#   feeding the fields in this file.
#
# WHO USES IT:
#   dependencies.py     - takes database_url and redis_url
#   main.py             - takes app_name, log_level, cors_origins
#   routes/tickets.py   - takes the ai_analysis_* feature switches
#   packages/model_gateway/... - takes every model_* setting
# ============================================================================

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# Each line below is one setting: its name, the type of value it must be, and
# the default used when nothing is supplied. Because a type is declared, the
# library also converts and checks the value for you — environment variables
# always arrive as text, so "true" becomes a real True, and "30.0" becomes a
# real number. A bad value (e.g. MODEL_TIMEOUT_SECONDS=abc) makes the app
# refuse to start, which is deliberate: better to fail loudly at boot than to
# behave strangely later.
class Settings(BaseSettings):
    app_name: str = "supportops-ai-copilot"   # shown in the auto-generated API docs page
    app_env: str = "local"                    # "local" / "staging" / "production" label
    log_level: str = "INFO"                   # how chatty the logs are (DEBUG shows the most)

    # --- Where the two data stores live ---
    # This long string is a "connection URL". Read it as:
    #   postgresql:// username : password @ host : port / database-name
    database_url: str = "postgresql://supportops:supportops@localhost:5432/supportops"
    # Redis is the fast in-memory store holding the queue of AI jobs waiting to
    # be processed. The trailing "/0" picks database number 0 inside Redis.
    redis_url: str = "redis://localhost:6379/0"

    # Web browsers refuse to let a page at one address call an API at a
    # different address, unless the API says it is allowed. This is called CORS
    # (Cross-Origin Resource Sharing). List the allowed web page addresses here,
    # separated by commas. Empty means "allow nothing", which is the safe
    # default. Used by _add_cors_middleware in main.py.
    cors_origins: str = ""

    # --- Feature switches for the AI ---
    # These let the AI be turned on gradually rather than all at once, which is
    # how a risky new feature gets rolled out safely. Checked in
    # apps/api/supportops_api/checks.py.
    ai_analysis_enabled: bool = True           # the master on/off switch
    ai_analysis_enabled_tenants: str = ""      # comma-separated; empty means "all companies"
    ai_analysis_enabled_categories: str = ""   # comma-separated; empty means "all ticket types"

    # --- Which AI model to use, and what it costs ---
    # "mock" means: don't call a real AI at all, just return canned answers.
    # That keeps tests fast, free, and predictable. Switching this to "hosted"
    # makes it call a real paid service instead. The choice is acted on in
    # packages/model_gateway/supportops_model_gateway/routing.py.
    model_provider: str = "mock"
    model_api_key: str = ""                          # the secret password for the AI service.
                                                     # NEVER write a real key in this file —
                                                     # supply it as an environment variable.
    model_name: str = "gpt-5.6"                      # which specific model to ask
    model_base_url: str = "https://api.openai.com/v1"  # the AI service's web address
    model_timeout_seconds: float = 30.0              # give up if it hasn't answered in 30s, so
                                                     # one slow call can't block things forever
    model_max_output_tokens: int = 1200              # cap on answer length. A "token" is roughly
                                                     # three-quarters of a word — AI services bill
                                                     # by the token, so this caps the cost too.

    # What we are charged per 1,000 tokens. These are only used for the running
    # cost total shown on the metrics page — they don't affect what the AI does.
    # Left at 0.0 by default because the mock provider is free.
    # Used by packages/model_gateway/supportops_model_gateway/cost.py.
    model_input_cost_per_1k_tokens: float = 0.0      # price for text we SEND
    model_output_cost_per_1k_tokens: float = 0.0     # price for text we GET BACK (usually dearer)

    # Configuration for the settings system itself, not an app setting:
    #   env_file=".env"   -> also read values from a local file called .env
    #   extra="ignore"    -> if the environment contains variables we don't
    #                        recognise, quietly ignore them instead of crashing
    #                        (important, since a server's environment is always
    #                        full of unrelated variables like PATH and HOME)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Reads the settings once, then hands back that same result forever after.
#
# "@lru_cache" is what makes that happen. Two reasons it matters here:
#   1. Speed — no re-reading files and environment variables on every request.
#   2. Consistency — every part of the app is guaranteed to be looking at
#      exactly the same settings object, so they can never disagree.
#
# Side effect worth knowing: because it is cached, changing an environment
# variable while the app is running has no effect. You must restart the app.
@lru_cache
def get_settings() -> Settings:
    return Settings()
