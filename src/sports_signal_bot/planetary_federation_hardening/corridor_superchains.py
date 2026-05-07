from typing import List
from .contracts import (
    CorridorSuperchainRecord, SuperchainFamily, SuperchainStatus,
    SuperchainSegmentRecord, CorridorSuperchainHealthRecord,
    CorridorSuperchainWarningRecord, SuperchainReplayRecord, SuperchainLineageRecord
)
from dataclasses import dataclass

@dataclass
class SuperchainCheckpointRecord:
    checkpoint_id: str
    family: str

def build_corridor_superchain(superchain_id: str, family: SuperchainFamily) -> CorridorSuperchainRecord:
    return CorridorSuperchainRecord(
        corridor_superchain_id=superchain_id,
        superchain_family=family
    )

def add_superchain_segment(superchain: CorridorSuperchainRecord, segment: SuperchainSegmentRecord) -> None:
    superchain.segment_refs.append(segment)

def verify_corridor_superchain(superchain: CorridorSuperchainRecord) -> CorridorSuperchainHealthRecord:
    stale_segments = [s for s in superchain.segment_refs if s.is_stale]
    unsupported_replay = [r for r in superchain.replay_refs if not r.is_supported]
    broken_lineage = [l for l in superchain.lineage_refs if not l.preserved]

    if stale_segments:
        superchain.superchain_status = SuperchainStatus.SUPERCHAIN_CAVEATED
        superchain.warnings.append(CorridorSuperchainWarningRecord(warning_id="stale_segments", description="Stale segments found"))
        return CorridorSuperchainHealthRecord(is_healthy=False, status=SuperchainStatus.SUPERCHAIN_CAVEATED)

    if unsupported_replay or broken_lineage:
        superchain.superchain_status = SuperchainStatus.SUPERCHAIN_BROKEN
        superchain.warnings.append(CorridorSuperchainWarningRecord(warning_id="broken_integrity", description="Lineage broken or replay unsupported"))
        return CorridorSuperchainHealthRecord(is_healthy=False, status=SuperchainStatus.SUPERCHAIN_BROKEN)

    if not superchain.segment_refs:
        superchain.superchain_status = SuperchainStatus.SUPERCHAIN_GAPPED
        return CorridorSuperchainHealthRecord(is_healthy=False, status=SuperchainStatus.SUPERCHAIN_GAPPED)

    superchain.superchain_status = SuperchainStatus.SUPERCHAIN_VERIFIED
    return CorridorSuperchainHealthRecord(is_healthy=True, status=SuperchainStatus.SUPERCHAIN_VERIFIED)

def replay_corridor_superchain(superchain: CorridorSuperchainRecord) -> bool:
    return superchain.superchain_status == SuperchainStatus.SUPERCHAIN_VERIFIED

def summarize_corridor_superchain(superchain: CorridorSuperchainRecord) -> dict:
    return {
        "id": superchain.corridor_superchain_id,
        "family": superchain.superchain_family.value,
        "status": superchain.superchain_status.value,
        "warnings_count": len(superchain.warnings)
    }

def create_superchain_checkpoint(checkpoint_id: str, family: str) -> SuperchainCheckpointRecord:
    return SuperchainCheckpointRecord(checkpoint_id=checkpoint_id, family=family)

def diff_superchain_replay(superchain: CorridorSuperchainRecord) -> dict:
    return {"diffs": []}

def detect_superchain_gaps(superchain: CorridorSuperchainRecord) -> List[str]:
    if not superchain.segment_refs:
        return ["missing_segments"]
    return []

def summarize_superchain_segments(segments: List[SuperchainSegmentRecord]) -> dict:
    return {
        "total": len(segments),
        "stale": sum(1 for s in segments if s.is_stale)
    }
