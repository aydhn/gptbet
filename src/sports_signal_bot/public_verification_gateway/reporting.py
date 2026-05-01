from typing import Dict, List, Any
from .contracts import PublicVerificationSummaryRecord

def compute_disclosure_coverage(
    total_bundles: int,
    published_bundles: int
) -> str:
    if total_bundles == 0:
        return "sparse"

    rate = published_bundles / total_bundles

    if rate < 0.2:
        return "sparse"
    if rate < 0.5:
        return "partial"
    if rate < 0.8:
        return "good"
    if rate < 0.95:
        return "strong"
    return "audit_ready"

def summarize_coverage_gaps(
    published_families: List[str],
    required_families: List[str]
) -> List[str]:
    return [f for f in required_families if f not in published_families]

def generate_kpi_summary(
    total_bundles: int,
    publish_ready: int,
    redaction_success: int,
    total_intakes: int,
    accepted_intakes: int,
    malformed_intakes: int
) -> Dict[str, Any]:
    return {
        "publish_ready_bundle_rate": publish_ready / max(1, total_bundles),
        "disclosure_redaction_success_rate": redaction_success / max(1, total_bundles),
        "challenge_intake_acceptance_rate": accepted_intakes / max(1, total_intakes),
        "malformed_intake_rate": malformed_intakes / max(1, total_intakes)
    }
