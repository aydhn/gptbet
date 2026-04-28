from sports_signal_bot.release_management.canary import CanaryValidator
from sports_signal_bot.release_management.contracts import CanaryHealthSnapshot, CanaryResult

def test_canary_validator():
    validator = CanaryValidator()

    health = CanaryHealthSnapshot(health_score=95.0, anomalies=0)
    res = validator.evaluate_canary(
        run_id="run1",
        canary_chain_id="c2",
        stable_chain_id="c1",
        canary_metrics={"logloss": 0.50},
        stable_metrics={"logloss": 0.52},
        health_snapshot=health
    )

    assert res.result == CanaryResult.pass_

    # Degraded metrics
    res2 = validator.evaluate_canary(
        run_id="run2",
        canary_chain_id="c3",
        stable_chain_id="c1",
        canary_metrics={"logloss": 0.60},
        stable_metrics={"logloss": 0.52},
        health_snapshot=health
    )

    assert res2.result == CanaryResult.fail
