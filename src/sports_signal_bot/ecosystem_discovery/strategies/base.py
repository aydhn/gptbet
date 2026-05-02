from abc import ABC, abstractmethod
from typing import List
from sports_signal_bot.ecosystem_discovery.contracts import (
    DiscoveryQueryRecord,
    DiscoveryResultRecord,
    CatalogEntryRecord
)

class BaseEcosystemDiscoveryStrategy(ABC):
    @abstractmethod
    def run_discovery(self, query: DiscoveryQueryRecord, available: List[CatalogEntryRecord]) -> DiscoveryResultRecord:
        pass
