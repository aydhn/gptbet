from datetime import datetime, timezone
from typing import List
from .contracts import SovereignPolicyConformancePackRecord, ConformancePackGapRecord


def classify_conformance_pack_gaps(
    pack: SovereignPolicyConformancePackRecord,
) -> List[ConformancePackGapRecord]:
    gaps = []

    for missing_dim in pack.missing_dimensions:
        # Simplistic mapping of dim -> gap type
        gap_type = f"missing_{missing_dim}"
        is_blocking = True  # Required dimensions map to blocking gaps

        gaps.append(
            ConformancePackGapRecord(
                gap_type=gap_type,
                dimension_ref=missing_dim,
                is_blocking=is_blocking,
                description=f"Required dimension {missing_dim} is missing evidence.",
            )
        )

    return gaps


def compute_pack_status(pack: SovereignPolicyConformancePackRecord) -> str:
    now = datetime.now(timezone.utc)
    if pack.validity_window.valid_until < now:
        return "expired"

    blocking = [g for g in pack.blocking_gaps if g.is_blocking]
    if blocking:
        return "blocked_by_gap"

    if not pack.missing_dimensions and not blocking:
        if pack.warnings:
            return "conformant_with_caveats"
        return "conformant"

    return "nonconformant"


def cap_pack_strength_due_to_gap(
    pack: SovereignPolicyConformancePackRecord, max_allowed_status: str
) -> SovereignPolicyConformancePackRecord:
    # E.g., if max_allowed_status is "conformant_with_caveats", force it down if it's "conformant"
    if pack.conformance_status == "conformant" and max_allowed_status != "conformant":
        pack.conformance_status = max_allowed_status
        pack.warnings.append(
            f"Strength capped to {max_allowed_status} due to policy gap constraints."
        )
    return pack


def explain_pack_gap_burden(pack: SovereignPolicyConformancePackRecord) -> str:
    if not pack.blocking_gaps:
        return f"Pack {pack.conformance_pack_id} has no blocking gaps."

    gap_descriptions = [g.description for g in pack.blocking_gaps if g.is_blocking]
    return f"Pack {pack.conformance_pack_id} is blocked by gaps: " + ", ".join(
        gap_descriptions
    )
