import pytest
from sports_signal_bot.simulation.sandbox import create_sandbox_namespace, apply_sandbox_patch, revoke_sandbox_patch
from sports_signal_bot.simulation.patches import build_candidate_patch

def test_sandbox_isolation():
    ns = create_sandbox_namespace("req_1")
    assert ns.namespace_id == "sandbox_req_1"
    assert len(ns.state.active_overrides) == 0

    patch = build_candidate_patch({"suggestion_id": "s1", "target_component_family": "provider_priority"})
    override = apply_sandbox_patch(ns, patch)

    assert len(ns.state.active_overrides) == 1
    assert ns.state.active_overrides[0] == override.override_id

    revoke_sandbox_patch(ns, override.override_id)
    assert len(ns.state.active_overrides) == 0
