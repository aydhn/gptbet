import yaml
from pathlib import Path
from sports_signal_bot.probabilistic.basketball.contracts import BasketballDistributionConfig

def load_basketball_config(config_path: str = "configs/probabilistic/basketball.yaml") -> BasketballDistributionConfig:
    p = Path(config_path)
    if not p.exists():
        return BasketballDistributionConfig()
    with open(p, "r") as f:
        data = yaml.safe_load(f)
        if data:
            return BasketballDistributionConfig(**data)
    return BasketballDistributionConfig()
