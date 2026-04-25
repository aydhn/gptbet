from typing import Dict, List, Optional

from sports_signal_bot.features.base import BaseFeatureBuilder


class FeatureRegistry:
    def __init__(self):
        self._builders: Dict[str, BaseFeatureBuilder] = {}

    def register(self, builder: BaseFeatureBuilder):
        self._builders[builder.name] = builder

    def list_builders(self, sport: Optional[str] = None) -> List[BaseFeatureBuilder]:
        if sport is None:
            return list(self._builders.values())
        return [
            b
            for b in self._builders.values()
            if sport in b.supported_sports or "all" in b.supported_sports
        ]

    def select_by_family(
        self, family: str, sport: Optional[str] = None
    ) -> List[BaseFeatureBuilder]:
        builders = self.list_builders(sport=sport)
        return [b for b in builders if b.family == family]

    def get_builder(self, name: str) -> Optional[BaseFeatureBuilder]:
        return self._builders.get(name)
