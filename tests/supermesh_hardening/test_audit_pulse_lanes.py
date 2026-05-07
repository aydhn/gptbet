from src.sports_signal_bot.supermesh_hardening.audit_pulse_lanes import build_global_audit_pulse_lane, emit_audit_pulse
from src.sports_signal_bot.supermesh_hardening.contracts import AuditPulseRecord

def test_build_global_audit_pulse_lane():
    lane = build_global_audit_pulse_lane("pl1", "worldwide_follow_the_sun_pulse_lane")
    assert lane.global_audit_pulse_lane_id == "pl1"
    assert lane.lane_status == "lane_verified"

def test_stale_pulse_caveats_lane():
    lane = build_global_audit_pulse_lane("pl1", "worldwide_follow_the_sun_pulse_lane")
    emit_audit_pulse(lane, AuditPulseRecord(pulse_id="p1", pulse_family="operator_pulse", is_stale=True))
    assert lane.lane_status == "lane_caveated"
