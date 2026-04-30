import pytest
from sports_signal_bot.simulation.contracts import SimulationComparisonRecord, ComparisonStatus, MaterialityBand, ComparisonUniverseRecord
from sports_signal_bot.simulation.recommendations import generate_recommendation, RecommendationType
import uuid

def test_recommendation_engine():
    comp = SimulationComparisonRecord(
        comparison_id="comp_1",
        baseline_snapshot_id="b1",
        variant_snapshot_id="v1",
        universe_record=ComparisonUniverseRecord(universe_id="u1", is_identical=True, sample_size=100),
        metrics=[],
        materiality_band=MaterialityBand.LARGE,
        materiality_score=20.0,
        status=ComparisonStatus.IMPROVED
    )

    rec = generate_recommendation(comp)
    assert rec.recommendation == RecommendationType.SAFE_FOR_REVIEW
