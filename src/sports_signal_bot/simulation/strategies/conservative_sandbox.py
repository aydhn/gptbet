from .base import BaseSimulationStrategy
from ..contracts import SimulationRunRecord, SimulationRequestRecord, CandidatePatchRecord, ComparisonStatus, MaterialityBand
from ..sandbox import create_sandbox_namespace, apply_sandbox_patch
from ..baseline import build_baseline_snapshot
from ..variant import build_variant_snapshot
from ..comparisons import compute_before_after_metrics, validate_comparison_universe
from ..contracts import SimulationComparisonRecord
from ..materiality import compute_materiality_score, classify_materiality_band
from ..recommendations import generate_recommendation
from datetime import datetime
import uuid

class ConservativeSandboxStrategy(BaseSimulationStrategy):
    def run_simulation(self, request: SimulationRequestRecord, patch: CandidatePatchRecord) -> SimulationRunRecord:
        run_id = f"run_{uuid.uuid4().hex[:8]}"
        started_at = datetime.utcnow()

        # 1. Setup Sandbox
        ns = create_sandbox_namespace(request.request_id)
        apply_sandbox_patch(ns, patch)

        # 2. Mock execution data (in a real system, invoke actual components)
        baseline_data = {"sample_size": 100, "metrics": {"hit_rate": 0.50, "dispute_count": 10}, "decision_counts": {"approved": 50}}
        variant_data = {"sample_size": 100, "metrics": {"hit_rate": 0.52, "dispute_count": 8}, "decision_counts": {"approved": 52}}

        # 3. Build snapshots
        baseline = build_baseline_snapshot(request.request_id, baseline_data)
        variant = build_variant_snapshot(request.request_id, variant_data)

        # 4. Compare
        universe = validate_comparison_universe(baseline_data, variant_data)
        metrics = compute_before_after_metrics(baseline, variant)
        mat_score = compute_materiality_score(metrics)
        mat_band = classify_materiality_band(mat_score)

        comp_record = SimulationComparisonRecord(
            comparison_id=f"comp_{uuid.uuid4().hex[:8]}",
            baseline_snapshot_id=baseline.snapshot_id,
            variant_snapshot_id=variant.snapshot_id,
            universe_record=universe,
            metrics=metrics,
            materiality_score=mat_score,
            materiality_band=mat_band,
            status=ComparisonStatus.IMPROVED if variant_data["metrics"]["hit_rate"] > baseline_data["metrics"]["hit_rate"] else ComparisonStatus.DEGRADED
        )

        # 5. Recommendation
        rec = generate_recommendation(comp_record)

        return SimulationRunRecord(
            run_id=run_id,
            request_id=request.request_id,
            status="completed",
            comparison=comp_record,
            recommendation=rec,
            started_at=started_at,
            completed_at=datetime.utcnow()
        )
