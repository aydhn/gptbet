import pytest
from sports_signal_bot.concurrency_hardening.ordering import build_async_ordering_graph, validate_async_ordering, detect_ordering_violation

def test_build_async_ordering_graph():
    graph = build_async_ordering_graph("target_a", {"deterministic_merge": True, "expected_sequence": ["a", "b"]})
    assert graph.status == "ordering_safe"
    assert len(graph.warnings) == 0

def test_validate_async_ordering():
    graph = build_async_ordering_graph("target_a", {"deterministic_merge": True, "expected_sequence": ["a", "b"]})
    assert validate_async_ordering(graph, ["a", "c", "b"]) == True
    assert validate_async_ordering(graph, ["b", "a"]) == False

def test_detect_ordering_violation():
    graph = build_async_ordering_graph("target_a", {"deterministic_merge": True, "expected_sequence": ["a", "b"]})
    violation = detect_ordering_violation(graph, ["b", "a"])
    assert violation is not None
