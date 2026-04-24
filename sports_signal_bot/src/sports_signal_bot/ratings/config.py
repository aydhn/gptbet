import yaml
from pathlib import Path
from sports_signal_bot.ratings.contracts import RatingConfig
from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.core.paths import get_project_root

logger = get_logger(__name__)

def load_rating_config(sport: str, custom_path: str = None) -> RatingConfig:
    root = get_project_root()
    base_dir = root / "configs" / "ratings"
    path = Path(custom_path) if custom_path else base_dir / f"{sport}.yaml"
    if not custom_path and not path.exists(): path = base_dir / "default.yaml"
    if not path.exists(): return RatingConfig()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return RatingConfig(**data)
    except Exception:
        return RatingConfig()
