from typing import List, Dict
import uuid
from .contracts import (
    FrozenBaselineRecord,
    BaselineScopeRecord,
    BaselineInputRecord,
    BaselineDriftRecord,
    BaselineResidueRecord
)

def build_frozen_baseline(family: str, inputs: List[BaselineInputRecord], scopes: List[BaselineScopeRecord]) -> FrozenBaselineRecord:
    return FrozenBaselineRecord(
        frozen_baseline_id=str(uuid.uuid4()),
        baseline_family=family, # type: ignore
        input_refs=inputs,
        scope_refs=scopes,
        baseline_status="baseline_verified"
    )

def verify_frozen_baseline(baseline: FrozenBaselineRecord) -> bool:
    if any(f.is_stale for f in baseline.freshness_refs):
        return False
    if any(d.hidden for d in baseline.drift_refs):
        return False
    return True

def summarize_frozen_baseline(baseline: FrozenBaselineRecord) -> Dict:
    return {
        "id": baseline.frozen_baseline_id,
        "family": baseline.baseline_family,
        "status": baseline.baseline_status,
        "scopes_count": len(baseline.scope_refs),
        "inputs_count": len(baseline.input_refs)
    }

def detect_baseline_drift(baseline: FrozenBaselineRecord) -> List[BaselineDriftRecord]:
    return baseline.drift_refs
