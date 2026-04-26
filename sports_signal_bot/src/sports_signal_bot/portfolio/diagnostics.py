import json
from typing import Dict, Any
from sports_signal_bot.portfolio.contracts import PortfolioRunManifest

def save_portfolio_manifest(manifest: PortfolioRunManifest, path: str):
    with open(path, "w") as f:
        # Pydantic V2 compat for dict
        try:
            data = manifest.model_dump(mode='json')
        except AttributeError:
            data = manifest.dict()

        json.dump(data, f, indent=2, default=str)
