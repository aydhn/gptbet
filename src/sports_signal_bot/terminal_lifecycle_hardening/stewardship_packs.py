from .contracts import (
    LongHorizonStewardshipPackRecord, PackFamily, PackStatus,
    StewardshipOwnerRecord, LongHorizonStewardshipWarningRecord
)
from typing import List, Dict, Any
import uuid

def build_long_horizon_stewardship_pack(
    family: PackFamily,
    owners: List[StewardshipOwnerRecord]
) -> LongHorizonStewardshipPackRecord:
    warnings = []

    if not owners:
        warnings.append(LongHorizonStewardshipWarningRecord(warning_id=str(uuid.uuid4()), message="Stewardship pack missing owners"))

    status = PackStatus.pack_verified
    if warnings:
        status = PackStatus.pack_caveated

    return LongHorizonStewardshipPackRecord(
        stewardship_pack_id=str(uuid.uuid4()),
        pack_family=family,
        owner_refs=owners,
        pack_status=status,
        warnings=warnings
    )

def summarize_long_horizon_stewardship_pack(pack: LongHorizonStewardshipPackRecord) -> Dict[str, Any]:
    return {
        "pack_id": pack.stewardship_pack_id,
        "family": pack.pack_family.value,
        "status": pack.pack_status.value,
        "owner_count": len(pack.owner_refs),
        "warning_count": len(pack.warnings)
    }
