from typing import Dict, Any, List
from .contracts import FailureSignatureRecord

def build_failure_signature(signals: Dict[str, Any]) -> FailureSignatureRecord:
    return FailureSignatureRecord(
        source_family=signals.get("source_family"),
        event_families=signals.get("event_families", []),
        lag_profile=signals.get("lag_profile"),
        trust_drift_profile=signals.get("trust_drift_profile"),
        replay_mismatch_burden=signals.get("replay_mismatch_burden"),
        swarm_agreement_status=signals.get("swarm_agreement_status"),
        relay_health_status=signals.get("relay_health_status"),
        routing_instability_markers=signals.get("routing_instability_markers", []),
        degraded_mode_transitions=signals.get("degraded_mode_transitions", []),
        quarantine_pressure=signals.get("quarantine_pressure"),
        freshness_decay_shape=signals.get("freshness_decay_shape"),
        conformance_blockers=signals.get("conformance_blockers", []),
    )

def normalize_signature_dimensions(signature: FailureSignatureRecord) -> FailureSignatureRecord:
    # Example normalization logic
    return signature

def compare_failure_signatures(sig1: FailureSignatureRecord, sig2: FailureSignatureRecord) -> float:
    # A simple matching algorithm for demonstration
    score = 0.0
    total_weights = 0.0

    if sig1.source_family and sig2.source_family:
        total_weights += 1.0
        if sig1.source_family == sig2.source_family:
            score += 1.0

    if sig1.swarm_agreement_status and sig2.swarm_agreement_status:
        total_weights += 1.0
        if sig1.swarm_agreement_status == sig2.swarm_agreement_status:
            score += 1.0

    return score / total_weights if total_weights > 0 else 0.0

def explain_signature_similarity(sig1: FailureSignatureRecord, sig2: FailureSignatureRecord) -> str:
    return f"Compared source_family and swarm_agreement_status. Match score: {compare_failure_signatures(sig1, sig2):.2f}"
