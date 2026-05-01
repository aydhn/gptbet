from typing import Dict, Any, List
from .contracts import ExchangeReadinessRecord
import uuid
import datetime

def extend_public_style_readiness(base_metrics: Dict[str, float], new_metrics: Dict[str, float]) -> Dict[str, float]:
    extended = base_metrics.copy()
    extended.update(new_metrics)
    return extended

def score_exchange_readiness(metrics: Dict[str, float]) -> float:
    # Example logic
    return metrics.get("packet_completeness", 0.0) * 0.4 + metrics.get("responder_diversity", 0.0) * 0.6

def score_notarization_readiness(metrics: Dict[str, float]) -> float:
    return metrics.get("notarization_coverage", 0.0)

def score_external_audit_operability(metrics: Dict[str, float]) -> float:
    score = score_exchange_readiness(metrics) * 0.5 + score_notarization_readiness(metrics) * 0.5
    return min(100.0, max(0.0, score))

def summarize_readiness_progress(record: ExchangeReadinessRecord) -> str:
    return f"Readiness Status: {record.status}, Score: {record.score}"

def generate_exchange_readiness_record(metrics: Dict[str, float]) -> ExchangeReadinessRecord:
    score = score_external_audit_operability(metrics)
    status = "internal_only_ready"
    if score > 80:
        status = "advanced_public_style_readiness"
    elif score > 60:
        status = "independent_audit_ready_candidate"
    elif score > 40:
        status = "external_exchange_ready"

    return ExchangeReadinessRecord(
        readiness_id=str(uuid.uuid4()),
        status=status,
        dimensions=metrics,
        score=score
    )
