import pytest
from sports_signal_bot.overlay_mesh_governance import (
    apply_controller_caps_to_route_governance,
    ControllerTierCapRecord
)

def test_controller_caps():
    cap = ControllerTierCapRecord(cap_id="c1", tier_ref="t1", cap_reason="degraded")
    res = apply_controller_caps_to_route_governance("r1", [cap])
    assert res == "capped_to_review_only"

    res2 = apply_controller_caps_to_route_governance("r2", [])
    assert res2 == "unbounded"
