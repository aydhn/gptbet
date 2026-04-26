from sports_signal_bot.thresholds.constraints import ConstraintEvaluator
from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord

def test_constraint_evaluator():
    config = {
        "minimum_accepted_count": 5,
        "minimum_coverage_rate": 0.2,
        "maximum_average_uncertainty": 0.5,
        "minimum_average_edge": 0.01,
        "maximum_log_loss": 0.8
    }
    evaluator = ConstraintEvaluator(config)

    cand = ThresholdCandidateRecord(
        market_type="1x2",
        sport="football",
        score_threshold=0.5,
        accepted_count=10,
        rejected_count=10,
        coverage_rate=0.5,
        acceptance_rate=0.5,
        average_uncertainty_penalty=0.2,
        average_edge=0.05
    )

    metrics = {"log_loss": 0.6}

    # Should pass all
    assert evaluator.check_constraints(cand, metrics) is True

    # Fail count
    cand.accepted_count = 2
    assert evaluator.check_constraints(cand, metrics) is False
    cand.accepted_count = 10

    # Fail uncertainty
    cand.average_uncertainty_penalty = 0.6
    assert evaluator.check_constraints(cand, metrics) is False
