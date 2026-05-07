from src.sports_signal_bot.supermesh_hardening.handoff_observatories import build_planetary_handoff_observatory, register_observatory_window
from src.sports_signal_bot.supermesh_hardening.contracts import HandoffObservatoryWindowRecord

def test_build_observatory():
    obs = build_planetary_handoff_observatory("obs1", "follow_the_sun_handoff_observatory")
    assert obs.planetary_handoff_observatory_id == "obs1"
    assert obs.observatory_status == "observatory_verified"

def test_ownerless_window_gaps_observatory():
    obs = build_planetary_handoff_observatory("obs1", "follow_the_sun_handoff_observatory")
    register_observatory_window(obs, HandoffObservatoryWindowRecord(window_id="w1", window_family="operator_to_operator_window", is_ownerless=True))
    assert obs.observatory_status == "observatory_gapped"
