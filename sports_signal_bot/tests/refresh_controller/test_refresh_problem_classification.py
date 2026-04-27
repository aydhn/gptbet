import pytest
from sports_signal_bot.refresh_controller.decisions import RefreshDecisionEngine
from sports_signal_bot.refresh_controller.states import ProblemClass

def test_classify_stale_artifact():
    engine = RefreshDecisionEngine()
    problems = engine.classify_refresh_problem({"stale_artifact_count": 5})
    assert len(problems) == 1
    assert problems[0].problem_class == ProblemClass.ARTIFACT_FRESHNESS

def test_classify_data_freshness():
    engine = RefreshDecisionEngine()
    problems = engine.classify_refresh_problem({"data_delay_seconds": 5000})
    assert len(problems) == 1
    assert problems[0].problem_class == ProblemClass.DATA_FRESHNESS

def test_classify_runtime_pipeline():
    engine = RefreshDecisionEngine()
    problems = engine.classify_refresh_problem({"global_health_score": 0.5})
    assert len(problems) == 1
    assert problems[0].problem_class == ProblemClass.RUNTIME_PIPELINE

def test_healthy():
    engine = RefreshDecisionEngine()
    problems = engine.classify_refresh_problem({"global_health_score": 0.9, "stale_artifact_count": 0, "data_delay_seconds": 10})
    assert len(problems) == 0
