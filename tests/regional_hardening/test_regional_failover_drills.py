# flake8: noqa: E501
from sports_signal_bot.regional_hardening.contracts import (
    FailoverResidueRecord,
    FailoverRollbackRecord,
    FailoverSourceRecord,
    FailoverTargetRecord,
    RegionalFailoverDrillFamily,
    RegionalFailoverDrillInputRecord,
    RegionalFailoverStatus,
)
from sports_signal_bot.regional_hardening.failover import build_regional_failover_drill


def test_build_regional_failover_drill():
    source = FailoverSourceRecord(
        region_id="reg1", region_type="primary", status="active", freshness_marker="m1"
    )
    target = FailoverTargetRecord(
        region_id="reg2", region_type="secondary", status="ready", readiness_marker="r1"
    )
    rollbacks = [FailoverRollbackRecord(rollback_id="rb1", readiness=True)]
    residues = [FailoverResidueRecord(residue_id="res1", is_hidden=False)]

    input_record = RegionalFailoverDrillInputRecord(
        drill_family=RegionalFailoverDrillFamily.primary_to_secondary_failover_drill,
        source=source,
        target=target,
        checkpoints=[],
        lags=[],
        rollbacks=rollbacks,
        residues=residues,
    )
    drill = build_regional_failover_drill(input_record)

    assert drill.failover_status == RegionalFailoverStatus.failover_ready


def test_failover_missing_markers():
    source = FailoverSourceRecord(
        region_id="reg1", region_type="primary", status="active", freshness_marker=""
    )
    target = FailoverTargetRecord(
        region_id="reg2", region_type="secondary", status="ready", readiness_marker="r1"
    )
    rollbacks = [FailoverRollbackRecord(rollback_id="rb1", readiness=True)]
    residues = [FailoverResidueRecord(residue_id="res1", is_hidden=False)]

    input_record = RegionalFailoverDrillInputRecord(
        drill_family=RegionalFailoverDrillFamily.primary_to_secondary_failover_drill,
        source=source,
        target=target,
        checkpoints=[],
        lags=[],
        rollbacks=rollbacks,
        residues=residues,
    )
    drill = build_regional_failover_drill(input_record)

    assert drill.failover_status == RegionalFailoverStatus.failover_gapped
