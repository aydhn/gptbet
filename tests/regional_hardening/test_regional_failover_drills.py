from sports_signal_bot.regional_hardening.failover import build_regional_failover_drill, verify_failover_source_and_target, evaluate_failover_lag
from sports_signal_bot.regional_hardening.contracts import (
    RegionalFailoverDrillFamily, FailoverSourceRecord, FailoverTargetRecord,
    FailoverCheckpointRecord, FailoverLagRecord, FailoverRollbackRecord,
    FailoverResidueRecord, RegionalFailoverStatus
)

def test_build_regional_failover_drill():
    source = FailoverSourceRecord(region_id="reg1", region_type="primary", status="active", freshness_marker="m1")
    target = FailoverTargetRecord(region_id="reg2", region_type="secondary", status="ready", readiness_marker="r1")
    rollbacks = [FailoverRollbackRecord(rollback_id="rb1", readiness=True)]
    residues = [FailoverResidueRecord(residue_id="res1", is_hidden=False)]

    drill = build_regional_failover_drill(
        RegionalFailoverDrillFamily.primary_to_secondary_failover_drill,
        source, target, [], [], rollbacks, residues
    )

    assert drill.failover_status == RegionalFailoverStatus.failover_ready

def test_failover_missing_markers():
    source = FailoverSourceRecord(region_id="reg1", region_type="primary", status="active", freshness_marker="")
    target = FailoverTargetRecord(region_id="reg2", region_type="secondary", status="ready", readiness_marker="r1")
    rollbacks = [FailoverRollbackRecord(rollback_id="rb1", readiness=True)]
    residues = [FailoverResidueRecord(residue_id="res1", is_hidden=False)]

    drill = build_regional_failover_drill(
        RegionalFailoverDrillFamily.primary_to_secondary_failover_drill,
        source, target, [], [], rollbacks, residues
    )

    assert drill.failover_status == RegionalFailoverStatus.failover_gapped
