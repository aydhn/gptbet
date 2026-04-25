# Shared utilities for the research phase


def get_default_research_config_path(sport: str) -> str:
    from sports_signal_bot.core.paths import get_configs_dir

    return str(get_configs_dir() / "research" / f"{sport}.yaml")
