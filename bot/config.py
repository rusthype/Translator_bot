import os


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ConfigError(f"Required environment variable {name!r} is not set")
    return value


def get_telegram_token() -> str:
    return _get_env("TELEGRAM_BOT_TOKEN")


def get_default_target_lang() -> str:
    return _get_env("DEFAULT_TARGET_LANG", "en")

