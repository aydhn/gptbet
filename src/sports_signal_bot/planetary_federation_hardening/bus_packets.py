from dataclasses import dataclass
from typing import List

@dataclass
class SchedulerBusOwnerRecord:
    owner_id: str

@dataclass
class SchedulerBusAckRecord:
    ack_id: str

@dataclass
class SchedulerBusReachabilityRecord:
    reachability_id: str

@dataclass
class SchedulerBusLagRecord:
    lag_id: str
    lag_ms: int

@dataclass
class SchedulerBusMismatchRecord:
    mismatch_id: str

@dataclass
class SchedulerBusRollbackRecord:
    rollback_id: str

@dataclass
class SchedulerBusHealthMarkerRecord:
    marker_id: str
