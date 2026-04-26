import pytest

from sports_signal_bot.thresholds.contracts import ThresholdPolicyRecord
from sports_signal_bot.thresholds.manifests import ThresholdManifestRecord


def test_threshold_manifest_record():
    policy = ThresholdPolicyRecord(
        policy_name="test_policy",
        sport="football",
        market_type="1x2",
        signal_strategy="score_only",
        threshold_type="min_score",
        selected_threshold=0.5,
        optimization_objective="balanced",
    )

    manifest = ThresholdManifestRecord(
        run_id="test_run",
        sport="football",
        market_type="1x2",
        best_policy=policy,
        total_evaluated_candidates=10,
        accepted_count=5,
        rejected_count=5,
    )

    assert manifest.run_id == "test_run"
    assert manifest.best_policy.policy_name == "test_policy"
    assert manifest.total_evaluated_candidates == 10
