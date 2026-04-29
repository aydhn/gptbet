from typing import Any, Dict, List, Optional

from sports_signal_bot.providers.adapters.base import ProviderAdapterBase


class ProviderRegistry:
    def __init__(self):
        self._adapters: Dict[str, ProviderAdapterBase] = {}

    def register(self, name: str, adapter: ProviderAdapterBase):
        self._adapters[name] = adapter

    def get(self, name: str) -> Optional[ProviderAdapterBase]:
        return self._adapters.get(name)

    def list_all(self) -> List[str]:
        return list(self._adapters.keys())
