from typing import Dict, Any, List
from .contracts import PerformanceEnvelopeRecord

def build_performance_envelope(envelope_id: str, family: str, target_ref: str, latency: float, memory: float, serialization: float, io_time: float, artifact_size: float, status: str = "within_budget") -> PerformanceEnvelopeRecord:
    return PerformanceEnvelopeRecord(
        performance_envelope_id=envelope_id,
        envelope_family=family,
        target_surface_ref=target_ref,
        latency_budget_ms=latency,
        memory_budget_mb=memory,
        serialization_budget_ms=serialization,
        io_budget_ms=io_time,
        artifact_size_budget_kb=artifact_size,
        envelope_status=status
    )

def measure_against_envelope(measurement: Dict[str, float], envelope: PerformanceEnvelopeRecord) -> str:
    if measurement.get("latency_ms", 0) > envelope.latency_budget_ms:
        return "over_budget"
    if measurement.get("memory_mb", 0) > envelope.memory_budget_mb:
        return "over_budget"
    return "within_budget"

def classify_budget_deviation(measurement: Dict[str, float], envelope: PerformanceEnvelopeRecord) -> Dict[str, Any]:
    deviations = {}
    if measurement.get("latency_ms", 0) > envelope.latency_budget_ms:
        deviations["latency"] = measurement["latency_ms"] - envelope.latency_budget_ms
    return deviations

def summarize_performance_envelope(envelopes: List[PerformanceEnvelopeRecord]) -> Dict[str, Any]:
    within = sum(1 for e in envelopes if e.envelope_status == "within_budget")
    over = sum(1 for e in envelopes if e.envelope_status == "over_budget")
    return {
        "total": len(envelopes),
        "within_budget": within,
        "over_budget": over
    }
