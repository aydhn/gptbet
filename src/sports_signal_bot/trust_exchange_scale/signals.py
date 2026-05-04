from typing import List, Dict, Any
from datetime import datetime
import uuid
from .contracts import (
    BenchmarkSignalEcosystemRecord, SignalEcosystemSourceRecord, SignalCorroborationRecord, SignalProvenanceRecord
)

def evaluate_signal_suppression(signals: List[Dict[str, Any]]) -> List[str]:
    suppressed = []
    for s in signals:
        if s.get("stale", False):
            suppressed.append(s["id"])
    return suppressed

def build_benchmark_signal_ecosystem(sources: List[Dict[str, Any]]) -> BenchmarkSignalEcosystemRecord:
    catalog = []
    corroboration = []
    provenance = []

    for src in sources:
        catalog.append(SignalEcosystemSourceRecord(
            signal_source_id=f"src-{uuid.uuid4().hex[:8]}",
            source_family=src.get("family", "unknown"),
            source_ref=src["id"],
            supported_signal_families=["benchmark"],
            provenance_confidence="moderate",
            freshness_state="stale" if src.get("stale") else "fresh",
            caveat_density=0.1,
            health_state="degraded" if src.get("stale") else "healthy",
            warnings=["stale_signal"] if src.get("stale") else []
        ))

        prov = SignalProvenanceRecord(
            provenance_id=f"prov-{uuid.uuid4().hex[:8]}",
            originating_baseline_ref="base-1",
            contributing_participant_refs=["part-1"],
            transformation_path=[],
            suppression_history=[],
            confidence_cap="bounded"
        )
        provenance.append(prov)

    # Mock corroboration
    if len(sources) > 1:
        corroboration.append(SignalCorroborationRecord(
            corroboration_id=f"corr-{uuid.uuid4().hex[:8]}",
            band="weakly_corroborated",
            corroborating_source_refs=[s["id"] for s in sources],
            conflicting_source_refs=[]
        ))

    suppressions = evaluate_signal_suppression(sources)

    return BenchmarkSignalEcosystemRecord(
        signal_ecosystem_id=f"eco-{uuid.uuid4().hex[:8]}",
        source_catalog_refs=catalog,
        active_signal_refs=[s["id"] for s in sources if s["id"] not in suppressions],
        corroboration_refs=corroboration,
        provenance_refs=provenance,
        suppression_refs=suppressions,
        health_status="caution" if suppressions else "healthy",
        warnings=["some_signals_suppressed"] if suppressions else []
    )
