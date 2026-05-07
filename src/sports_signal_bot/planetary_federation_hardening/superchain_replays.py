from dataclasses import dataclass

@dataclass
class SuperchainOwnerRecord:
    owner_id: str

@dataclass
class SuperchainGapRecord:
    gap_id: str

@dataclass
class SuperchainDriftRecord:
    drift_id: str

@dataclass
class SuperchainMismatchRecord:
    mismatch_id: str

@dataclass
class SuperchainHealthMarkerRecord:
    marker_id: str
