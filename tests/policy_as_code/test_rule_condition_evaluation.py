import pytest
from sports_signal_bot.policy_as_code.evaluation import PolicyEvaluator

def test_rule_condition_evaluation_equals():
    evaluator = PolicyEvaluator()
    condition = {"namespace": "global", "field": "pressure", "operator": "==", "value": "critical"}
    context = {"global": {"pressure": "critical"}}
    assert evaluator.evaluate_condition(condition, context) is True

    context = {"global": {"pressure": "moderate"}}
    assert evaluator.evaluate_condition(condition, context) is False

def test_rule_condition_evaluation_less_than():
    evaluator = PolicyEvaluator()
    condition = {"namespace": "cohort.verification", "field": "clean_windows", "operator": "<", "value": 2}
    context = {"cohort": {"verification": {"clean_windows": 1}}}
    assert evaluator.evaluate_condition(condition, context) is True

    context = {"cohort": {"verification": {"clean_windows": 2}}}
    assert evaluator.evaluate_condition(condition, context) is False
