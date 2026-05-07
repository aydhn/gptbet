from dataclasses import dataclass
from typing import List

@dataclass
class CadenceHandoffRecord:
    handoff_id: str

@dataclass
class CadenceAckRecord:
    ack_id: str

@dataclass
class CadenceReachabilityRecord:
    reachability_id: str

@dataclass
class CadenceMismatchRecord:
    mismatch_id: str

@dataclass
class CadenceContinuityRecord:
    continuity_id: str

@dataclass
class CadenceDriftRecord:
    drift_id: str
    drift_ms: int

@dataclass
class CadenceHealthMarkerRecord:
    marker_id: str
