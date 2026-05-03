from datetime import datetime, timezone
import uuid
from typing import List, Dict, Tuple
from .contracts import (
    SovereignPolicyConformancePackRecord,
    ConformancePackDimensionRecord,
    ConformancePackEvidenceRecord,
    ConformancePackValidityRecord,
    ConformancePackGapRecord,
)
from .gaps import classify_conformance_pack_gaps, compute_pack_status


def evaluate_pack_dimensions(
    required_dimensions: List[ConformancePackDimensionRecord],
    provided_evidence: List[ConformancePackEvidenceRecord],
) -> Tuple[List[str], List[str]]:
    # Simple mock evaluation
    evidence_types = {e.evidence_type for e in provided_evidence}
    satisfied = []
    missing = []

    for dim in required_dimensions:
        if dim.dimension_name in evidence_types:
            satisfied.append(dim.dimension_name)
        elif dim.is_required:
            missing.append(dim.dimension_name)

    return satisfied, missing


def attach_pack_evidence(
    pack: SovereignPolicyConformancePackRecord,
    evidence: List[ConformancePackEvidenceRecord],
) -> SovereignPolicyConformancePackRecord:
    pack.evidence_refs.extend(evidence)
    # Re-evaluate
    satisfied, missing = evaluate_pack_dimensions(
        pack.required_dimensions, pack.evidence_refs
    )
    pack.satisfied_dimensions = satisfied
    pack.missing_dimensions = missing

    pack.blocking_gaps = classify_conformance_pack_gaps(pack)
    pack.conformance_status = compute_pack_status(pack)
    return pack


def build_policy_conformance_pack(
    target_scope_ref: str,
    required_dimensions: List[ConformancePackDimensionRecord],
    evidence: List[ConformancePackEvidenceRecord],
    valid_until: datetime,
    corridor_refs: List[str] = None,
    treaty_refs: List[str] = None,
) -> SovereignPolicyConformancePackRecord:

    now = datetime.now(timezone.utc)

    satisfied, missing = evaluate_pack_dimensions(required_dimensions, evidence)

    validity = ConformancePackValidityRecord(valid_from=now, valid_until=valid_until)

    pack = SovereignPolicyConformancePackRecord(
        conformance_pack_id=f"pack_{uuid.uuid4().hex[:8]}",
        target_scope_ref=target_scope_ref,
        corridor_refs=corridor_refs or [],
        treaty_refs=treaty_refs or [],
        required_dimensions=required_dimensions,
        satisfied_dimensions=satisfied,
        missing_dimensions=missing,
        evidence_refs=evidence,
        validity_window=validity,
        conformance_status="review_required",
    )

    pack.blocking_gaps = classify_conformance_pack_gaps(pack)
    pack.conformance_status = compute_pack_status(pack)

    return pack


def summarize_conformance_pack(pack: SovereignPolicyConformancePackRecord) -> dict:
    return {
        "pack_id": pack.conformance_pack_id,
        "status": pack.conformance_status,
        "required_count": len(pack.required_dimensions),
        "satisfied_count": len(pack.satisfied_dimensions),
        "missing_count": len(pack.missing_dimensions),
        "blocking_gaps_count": len([g for g in pack.blocking_gaps if g.is_blocking]),
    }
