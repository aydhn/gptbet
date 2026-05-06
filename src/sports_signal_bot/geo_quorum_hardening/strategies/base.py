from abc import ABC, abstractmethod
from src.sports_signal_bot.geo_quorum_hardening.contracts import GeoQuorumHardeningManifestRecord

class BaseGeoQuorumHardeningStrategy(ABC):
    @abstractmethod
    def evaluate(self, inputs: dict) -> GeoQuorumHardeningManifestRecord:
        pass
