import pytest
from sports_signal_bot.performance.cache_keys import build_cache_key
from sports_signal_bot.performance.cache_policies import resolve_cache_policy
from sports_signal_bot.performance.profiling import TimingRegistry, PerformanceTimer
from sports_signal_bot.performance.incremental import IncrementalEngine
from sports_signal_bot.performance.runner import PerformanceRunner

def test_cache_key_determinism():
    inputs1 = {"sport": "football", "market": "1x2"}
    inputs2 = {"market": "1x2", "sport": "football"}
    key1 = build_cache_key(inputs1)
    key2 = build_cache_key(inputs2)
    assert key1.key == key2.key

def test_cache_policy_resolution():
    policy = resolve_cache_policy("session_cache")
    assert policy["write"] is True

def test_step_profiling():
    registry = TimingRegistry()
    with PerformanceTimer("test_step", registry):
        pass
    records = registry.get_all()
    assert len(records) == 1
    assert records[0].step_name == "test_step"

def test_incremental_scope_detection():
    engine = IncrementalEngine()
    decision = engine.decide_full_vs_incremental(50, 100)
    assert decision.decision == "incremental_append"

def test_performance_runner():
    runner = PerformanceRunner()
    manifest = runner.run_pass()
    assert manifest is not None
    assert manifest.mode == "safe_default"
