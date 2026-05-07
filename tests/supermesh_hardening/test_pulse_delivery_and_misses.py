from src.sports_signal_bot.supermesh_hardening.pulse_deliveries import verify_pulse_handoff, detect_audit_pulse_gaps
from src.sports_signal_bot.supermesh_hardening.audit_pulse_lanes import build_global_audit_pulse_lane
from src.sports_signal_bot.supermesh_hardening.contracts import AuditPulseDeliveryRecord, AuditPulseMissRecord

def test_missing_ack_gaps_lane():
    lane = build_global_audit_pulse_lane("pl1", "worldwide_follow_the_sun_pulse_lane")
    delivery = AuditPulseDeliveryRecord(delivery_id="d1", pulse_ref="p1", has_ack=False)
    assert not verify_pulse_handoff(lane, delivery)
    assert lane.lane_status == "lane_gapped"

def test_hidden_miss_detected():
    lane = build_global_audit_pulse_lane("pl1", "worldwide_follow_the_sun_pulse_lane")
    miss = AuditPulseMissRecord(miss_id="m1", pulse_ref="p1", is_hidden=True)
    gaps = detect_audit_pulse_gaps(lane, [], [miss])
    assert "Gap: Hidden pulse miss m1" in gaps
