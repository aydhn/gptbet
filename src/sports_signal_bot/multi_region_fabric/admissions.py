from sports_signal_bot.multi_region_fabric.contracts import CrossRegionAdmissionRecord

ADMISSION_OUTCOMES = [
    "local_only_admitted",
    "review_only_external_visibility",
    "external_transfer_preparation_allowed",
    "failover_candidate_only",
    "cross_region_runtime_denied",
    "treaty_missing",
    "sovereignty_blocked",
    "revalidation_required"
]

def evaluate_cross_region_admission(lane_id: str, src: str, tgt: str, has_treaty: bool, has_sov: bool) -> CrossRegionAdmissionRecord:
    outcome = "external_transfer_preparation_allowed" if (has_treaty and has_sov) else "sovereignty_blocked"
    if not has_treaty and has_sov:
        outcome = "treaty_missing"
    return CrossRegionAdmissionRecord(
        admission_id=f"adm_{lane_id}",
        lane_id=lane_id,
        source_region=src,
        target_region=tgt,
        outcome=outcome,
        reasoning="Evaluated treaty and sovereignty"
    )

def require_reissue_or_local_token(lane_id: str) -> bool:
    return True

def validate_cross_region_closure_fit(lane_id: str) -> bool:
    return True

def summarize_admission_outcome(adm: CrossRegionAdmissionRecord) -> str:
    return f"Admission: {adm.outcome}"
