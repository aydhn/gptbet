from datetime import datetime

from sports_signal_bot.providers.quality import ProviderQualityScorer


def test_provider_quality_scoring():
    scorer = ProviderQualityScorer({"overall": 0.5, "freshness": 0.3})
    now = datetime.utcnow()
    res = scorer.score_payload([{"id": 1}], "fixtures", now)
    assert res.is_acceptable == True
    assert res.freshness_score == 1.0
    assert res.completeness_score == 1.0
    assert res.overall_score > 0.5
