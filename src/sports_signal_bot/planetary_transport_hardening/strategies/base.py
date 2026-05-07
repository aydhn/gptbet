import abc
from typing import Dict, Any, List
from ..contracts import PlanetaryCoverageBusRecord, IntercontinentalHandoffArchiveRecord, QuorumFederationCorridorRecord, WorldwideAuditCalendarSimulationRecord, PlanetaryTransportMatrix

class BasePlanetaryTransportHardeningStrategy(abc.ABC):
    @abc.abstractmethod
    def run_coverage_bus_pass(self, context: Dict[str, Any]) -> List[PlanetaryCoverageBusRecord]:
        pass

    @abc.abstractmethod
    def run_handoff_archive_pass(self, context: Dict[str, Any]) -> List[IntercontinentalHandoffArchiveRecord]:
        pass

    @abc.abstractmethod
    def run_quorum_corridor_pass(self, context: Dict[str, Any]) -> List[QuorumFederationCorridorRecord]:
        pass

    @abc.abstractmethod
    def run_audit_calendar_pass(self, context: Dict[str, Any]) -> List[WorldwideAuditCalendarSimulationRecord]:
        pass

    @abc.abstractmethod
    def generate_transport_matrix(self, context: Dict[str, Any]) -> PlanetaryTransportMatrix:
        pass
