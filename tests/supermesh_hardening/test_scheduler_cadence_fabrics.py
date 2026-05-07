from src.sports_signal_bot.supermesh_hardening.cadence_fabrics import build_scheduler_cadence_fabric, add_cadence_fabric_lane, verify_scheduler_cadence_fabric
from src.sports_signal_bot.supermesh_hardening.contracts import CadenceFabricLaneRecord

def test_build_scheduler_cadence_fabric():
    fab = build_scheduler_cadence_fabric("fab1", "planetary_coverage_cadence_fabric")
    assert fab.scheduler_cadence_fabric_id == "fab1"
    assert fab.fabric_status == "fabric_verified"

def test_critical_ownerless_lane_blocks_fabric():
    fab = build_scheduler_cadence_fabric("fab1", "planetary_coverage_cadence_fabric")
    add_cadence_fabric_lane(fab, CadenceFabricLaneRecord(lane_id="l1", lane_family="global_primary_lane", is_critical=True, is_ownerless=True))
    assert fab.fabric_status == "fabric_gapped"
    assert verify_scheduler_cadence_fabric(fab) == "fabric_gapped"
