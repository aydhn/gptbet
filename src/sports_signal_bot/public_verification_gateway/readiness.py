from typing import Dict, List, Any
from .contracts import (
    DisclosureBundleRecord,
    PublicPacketRecord,
    PublicVerificationSummaryRecord
)
from datetime import datetime

def collect_publication_readiness_blockers(
    index_entries: List[Any],
    quarantine_count: int,
    malformed_intake_rate: float
) -> List[str]:
    blockers = []

    if len(index_entries) == 0:
        blockers.append("No active index entries published")

    if quarantine_count > 10:
        blockers.append(f"High quarantine backlog ({quarantine_count})")

    if malformed_intake_rate > 0.3:
        blockers.append(f"High malformed intake rate ({malformed_intake_rate:.2f})")

    return blockers

def score_publication_maturity(
    index_entries: List[Any],
    quarantine_count: int,
    malformed_intake_rate: float
) -> str:
    blockers = collect_publication_readiness_blockers(index_entries, quarantine_count, malformed_intake_rate)

    if len(blockers) >= 1 and "No active index entries published" in blockers:
        return "internal_only"
    if len(blockers) > 0:
        return "limited_publication_ready"

    return "public_style_gateway_ready"

def compute_public_gateway_readiness(
    gateway_id: str,
    index_entries: List[Any],
    quarantine_count: int,
    metrics: Dict[str, Any]
) -> PublicVerificationSummaryRecord:

    malformed_intake_rate = metrics.get("malformed_intake_rate", 0.0)
    score = score_publication_maturity(index_entries, quarantine_count, malformed_intake_rate)

    return PublicVerificationSummaryRecord(
        summary_id=f"sum_readiness_{gateway_id}",
        generated_at=datetime.utcnow(),
        metrics=metrics,
        readiness_score=score
    )

def summarize_readiness_upgrade_paths(score: str, blockers: List[str]) -> List[str]:
    paths = []
    for b in blockers:
        paths.append(f"Resolve: {b}")

    if score == "internal_only":
        paths.append("Need to establish baseline publication index and reduce quarantine queue.")
    elif score == "limited_publication_ready":
        paths.append("Clear remaining blockers to achieve full public readiness.")

    return paths
