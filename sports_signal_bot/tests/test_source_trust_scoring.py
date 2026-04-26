import math

from sports_signal_bot.source_selection.metadata import (
    EvaluationMetadata,
    RefreshMetadata,
    SourceMetadataRecord,
)
from sports_signal_bot.source_selection.scoring import SourceTrustScorer


def test_trust_scoring_performance():
    scorer = SourceTrustScorer({"performance": 1.0})  # Isolate performance

    meta_good = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        eval_info=EvaluationMetadata(recent_log_loss=0.4),
    )
    assert scorer.compute_performance_component(meta_good) == 1.0

    meta_bad = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        eval_info=EvaluationMetadata(recent_log_loss=0.8),
    )
    assert scorer.compute_performance_component(meta_bad) == 0.0

    meta_mid = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        eval_info=EvaluationMetadata(recent_log_loss=0.6),
    )
    assert math.isclose(
        scorer.compute_performance_component(meta_mid), 0.5, rel_tol=1e-9
    )


def test_trust_scoring_stale_zeroes_recency():
    scorer = SourceTrustScorer({"recency": 1.0})
    meta = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        refresh_info=RefreshMetadata(is_stale_flag=True),
    )
    assert scorer.compute_recency_component(meta) == 0.0
