import pytest
from sports_signal_bot.concurrency_hardening.guards import build_concurrency_guard

def test_build_concurrency_guard_safe():
    guard = build_concurrency_guard(
        guard_family="shared_state_guard",
        protected_surface_ref="surface_1",
        scope_bounds={"type": "read_write"},
        owner="owner_A",
        ordering_rules={"order": "strict"},
        timeout_ms=5000,
        cancellation_policy="abort"
    )
    assert guard.guard_status == "guard_safe"
    assert len(guard.warnings) == 0

def test_build_concurrency_guard_unknown_family():
    guard = build_concurrency_guard(
        guard_family="unknown_guard",
        protected_surface_ref="surface_1",
        scope_bounds={},
        owner="owner_A",
        ordering_rules={},
        timeout_ms=5000,
        cancellation_policy="abort"
    )
    assert guard.guard_status == "guard_review_only"
    assert len(guard.warnings) == 1
    assert "Unknown guard family" in guard.warnings[0].message
