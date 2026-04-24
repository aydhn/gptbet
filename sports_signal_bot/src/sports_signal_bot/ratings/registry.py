from typing import Dict, Type
from sports_signal_bot.ratings.base import BaseRatingEngine
from sports_signal_bot.ratings.elo import EloRatingEngine
from sports_signal_bot.ratings.glicko_placeholder import GlickoPlaceholderEngine

class RatingEngineRegistry:
    def __init__(self):
        self._engines: Dict[str, Type[BaseRatingEngine]] = {"elo": EloRatingEngine, "glicko": GlickoPlaceholderEngine}
    def register(self, name: str, engine_cls: Type[BaseRatingEngine]):
        self._engines[name.lower()] = engine_cls
    def get_engine_class(self, name: str) -> Type[BaseRatingEngine]:
        name_lower = name.lower()
        if name_lower not in self._engines: raise ValueError(f"Unknown rating engine: {name}")
        return self._engines[name_lower]

RATING_ENGINE_REGISTRY = RatingEngineRegistry()
