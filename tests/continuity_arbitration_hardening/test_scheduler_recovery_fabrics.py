from src.sports_signal_bot.continuity_arbitration_hardening.contracts import RecoveryFabricPacketRecord
from src.sports_signal_bot.continuity_arbitration_hardening.recovery_fabrics import build_scheduler_recovery_fabric

def test_build_scheduler_recovery_fabric_fresh():
    packets = [RecoveryFabricPacketRecord(packet_id="1", payload_hash="hash", is_stale=False)]
    fabric = build_scheduler_recovery_fabric("test_fabric", packets)
    assert fabric.fabric_status == "fabric_verified"

def test_build_scheduler_recovery_fabric_stale():
    packets = [RecoveryFabricPacketRecord(packet_id="1", payload_hash="hash", is_stale=True)]
    fabric = build_scheduler_recovery_fabric("test_fabric", packets)
    assert fabric.fabric_status == "fabric_caveated"
