from typing import List, Dict, Any, Optional
from sports_signal_bot.overlay_mesh_governance.contracts import (
    ConsortiumSignalRecord,
    ConsortiumLayerRecord,
    ConsortiumCorroborationRecord,
    ConsortiumSignalConflictRecord
)

def ingest_consortium_signal(signal: ConsortiumSignalRecord) -> ConsortiumSignalRecord:
    # basic validation and ingestion
    return validate_consortium_signal(signal)

def validate_consortium_signal(signal: ConsortiumSignalRecord) -> ConsortiumSignalRecord:
    # Check basic invariants
    if signal.provenance_confidence.provenance_confidence < 0.1:
        signal.suppression_state = "suppressed"
    return signal

def correlate_signal_with_existing_layer(signal: ConsortiumSignalRecord, layer: ConsortiumLayerRecord) -> str:
    # determine where signal fits
    if signal.signal_family in layer.supported_signal_families:
        return "accepted"
    return "rejected"

def summarize_signal_ingestion(signals: List[ConsortiumSignalRecord]) -> Dict[str, Any]:
    return {
        "total_signals": len(signals),
        "suppressed": sum(1 for s in signals if s.suppression_state == "suppressed")
    }

def compute_consortium_corroboration(signals: List[ConsortiumSignalRecord]) -> ConsortiumCorroborationRecord:
    # A mock logic to compute corroboration
    if len(signals) > 3:
        return ConsortiumCorroborationRecord(corroboration_band="strongly_supported_but_caveated", corroborating_sources=[s.source_member for s in signals])
    elif len(signals) > 1:
        return ConsortiumCorroborationRecord(corroboration_band="boundedly_supported", corroborating_sources=[s.source_member for s in signals])
    return ConsortiumCorroborationRecord(corroboration_band="isolated", corroborating_sources=[s.source_member for s in signals])

def classify_consortium_conflicts(signals: List[ConsortiumSignalRecord]) -> List[ConsortiumSignalConflictRecord]:
    # Mock finding conflicts
    conflicts = []
    if len(signals) > 2:
        # simulate a conflict found
        conflicts.append(ConsortiumSignalConflictRecord(conflict_id="conf_1", description="Conflicting projections"))
    return conflicts

def cap_signal_strength_by_provenance(signal: ConsortiumSignalRecord) -> ConsortiumSignalRecord:
    if signal.provenance_confidence.provenance_confidence < 0.5:
        signal.corroboration_band.corroboration_band = "weakly_supported"
    return signal

def summarize_corroboration_state(signal: ConsortiumSignalRecord) -> Dict[str, Any]:
    return {
        "signal_id": signal.signal_id,
        "band": signal.corroboration_band.corroboration_band,
        "provenance": signal.provenance_confidence.provenance_confidence
    }

def suppress_consortium_signal(signal: ConsortiumSignalRecord, reason: str) -> ConsortiumSignalRecord:
    signal.suppression_state = "suppressed"
    # add to caveats/warnings or a specific suppression field in real implementation
    return signal

def downgrade_consortium_layer(layer: ConsortiumLayerRecord, reason: str) -> ConsortiumLayerRecord:
    layer.layer_status = "degraded"
    return layer

def explain_consortium_suppression(signal: ConsortiumSignalRecord) -> str:
    return f"Signal {signal.signal_id} is suppressed. Current state: {signal.suppression_state}"

def summarize_suppression_burden(signals: List[ConsortiumSignalRecord]) -> Dict[str, Any]:
    suppressed = [s for s in signals if s.suppression_state == "suppressed"]
    return {
        "total_suppressed": len(suppressed),
        "burden_ratio": len(suppressed) / len(signals) if signals else 0
    }
