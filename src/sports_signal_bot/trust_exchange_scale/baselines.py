from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone
import uuid
from .contracts import (
    SovereignResilienceGovernanceBaselineRecord, GovernanceBaselineDimensionRecord, GovernanceBaselineVersionRecord
)

def build_governance_baseline(family: str, drift: float) -> SovereignResilienceGovernanceBaselineRecord:
    dim = GovernanceBaselineDimensionRecord(
        dimension_name="sovereignty_override_visibility",
        required_alignment="strict",
        current_drift=drift
    )

    ver = GovernanceBaselineVersionRecord(
        version_id="v1.0",
        version_tag="stable",
        published_at=datetime.now(timezone.utc) - timedelta(days=30)
    )

    status = "aligned"
    warnings = []
    if drift > 0.2:
        status = "drifted"
        warnings.append("drift_exceeds_threshold")

    return SovereignResilienceGovernanceBaselineRecord(
        governance_baseline_id=f"base-{uuid.uuid4().hex[:8]}",
        baseline_family=family,
        applicable_scope_refs=["all"],
        dimension_refs=[dim],
        version_ref=ver,
        validity_window={"start": datetime.now(timezone.utc), "end": datetime.now(timezone.utc) + timedelta(days=90)},
        normalization_policy_ref="norm-1",
        baseline_status=status,
        warnings=warnings
    )

def summarize_baseline_governance_health(baselines: List[SovereignResilienceGovernanceBaselineRecord]) -> Dict[str, Any]:
    return {
        "total": len(baselines),
        "aligned": sum(1 for b in baselines if b.baseline_status == "aligned"),
        "drifted": sum(1 for b in baselines if b.baseline_status == "drifted")
    }
