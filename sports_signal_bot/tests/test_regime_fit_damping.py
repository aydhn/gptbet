from sports_signal_bot.source_selection.metadata import (RegimeProfileMetadata,
                                                         SourceMetadataRecord)
from sports_signal_bot.source_selection.scoring import SourceTrustScorer


def test_regime_fit_damping():
    scorer = SourceTrustScorer()

    # High sample size -> follows score closely
    meta_high = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        regime_profile=RegimeProfileMetadata(
            regime_scores={"r1": 0.9}, regime_sample_sizes={"r1": 100}
        ),
    )
    score_high = scorer.compute_regime_fit_component(meta_high, ["r1"])
    assert score_high == 0.9

    # Low sample size -> dampens towards 0.5
    meta_low = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        regime_profile=RegimeProfileMetadata(
            regime_scores={"r1": 0.9}, regime_sample_sizes={"r1": 10}
        ),
    )
    score_low = scorer.compute_regime_fit_component(meta_low, ["r1"])
    assert score_low < 0.9
    assert score_low > 0.5
