import re


def normalize_team_name(name: str) -> str:
    """Normalize a team name to a consistent format."""
    if not name:
        return ""
    name = name.strip()
    # Simple normalizations, like removing punctuation and extra spaces
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def normalize_league_name(name: str) -> str:
    if not name:
        return ""
    return name.strip().lower().replace(" ", "_")
