import pytest
from datetime import datetime, timezone
from sports_signal_bot.migration_hardening.contracts import (
    LaneFamily, CheckpointFamily, DrillFamily, ChainFamily, WarGameFamily,
    LaneStatus, ReadinessStatus, ChainStatus, WarGameStatus
)
from sports_signal_bot.migration_hardening.migration_lanes import (
    build_disaster_migration_lane, MigrationSourceRecord, verify_migration_source,
    MigrationCheckpointRecord, verify_migration_checkpoint, MigrationCutoverRecord,
    evaluate_migration_cutover_honesty, MigrationRollbackRecord
)
from sports_signal_bot.migration_hardening.team_coordination import (
    build_multi_team_coordination_drill, TeamRoleRecord, register_team_role,
    CoordinationHandoffRecord, execute_coordination_handoff, detect_coordination_gaps
)
from sports_signal_bot.migration_hardening.recovery_chains import (
    build_archival_recovery_chain, RecoveryChainNodeRecord, add_recovery_chain_node,
    RecoveryChainEdgeRecord, add_recovery_chain_edge, RecoveryChainDependencyRecord,
    verify_recovery_chain_integrity
)
from sports_signal_bot.migration_hardening.visibility_wargames import (
    build_governance_visibility_war_game, WarGameVisibilitySurfaceRecord,
    WarGameSignalRecord, inject_visibility_stress, detect_visibility_losses
)
from sports_signal_bot.migration_hardening.integration import MigrationHardeningOrchestrator

def test_migration_lane_stale_source():
    lane = build_disaster_migration_lane("l1", LaneFamily.archive_to_runtime_recovery_lane)
    src = MigrationSourceRecord(source_id="s1", freshness_timestamp=datetime.now(timezone.utc), is_stale=True)
    verify_migration_source(lane, src)
    assert lane.lane_status == LaneStatus.migration_blocked

def test_migration_cutover_dishonesty():
    lane = build_disaster_migration_lane("l1", LaneFamily.archive_to_runtime_recovery_lane)
    src = MigrationSourceRecord(source_id="s1", freshness_timestamp=datetime.now(timezone.utc), is_stale=False)
    lane.source_ref = src
    # No explicit rollback path
    cutover = MigrationCutoverRecord(cutover_id="c1")
    evaluate_migration_cutover_honesty(lane, cutover)
    assert cutover.is_honest == False
    assert lane.lane_status == LaneStatus.migration_blocked

def test_team_coordination_unacknowledged_handoff():
    drill = build_multi_team_coordination_drill("d1", DrillFamily.operator_reviewer_coordination_drill)
    r1 = TeamRoleRecord(role_id="r1", role_family="local_operator", owner="Alice")
    r2 = TeamRoleRecord(role_id="r2", role_family="governance_owner", owner="Bob")
    register_team_role(drill, r1)
    register_team_role(drill, r2)
    h1 = CoordinationHandoffRecord(handoff_id="h1", from_role="r1", to_role="r2", details="Handoff", is_acknowledged=False)
    execute_coordination_handoff(drill, h1)
    detect_coordination_gaps(drill)
    assert drill.readiness_status == ReadinessStatus.coordination_gapped

def test_recovery_chain_broken_dependency():
    chain = build_archival_recovery_chain("c1", ChainFamily.archive_restore_chain)
    dep = RecoveryChainDependencyRecord(dependency_id="d1", is_broken=True)
    chain.dependency_refs.append(dep)
    verify_recovery_chain_integrity(chain)
    assert chain.chain_status == ChainStatus.chain_broken

def test_visibility_wargame_loss_critical():
    game = build_governance_visibility_war_game("g1", WarGameFamily.no_safe_visibility_war_game)
    surf = WarGameVisibilitySurfaceRecord(surface_id="s1", maintains_no_safe=False)
    sig = WarGameSignalRecord(signal_id="sig1")
    inject_visibility_stress(game, surf, sig)
    detect_visibility_losses(game)
    assert game.war_game_status == WarGameStatus.visibility_lost
    assert any(l.is_critical for l in game.loss_refs)

def test_orchestrator():
    orchestrator = MigrationHardeningOrchestrator()
    orchestrator.run_all_simulations()
    summary = orchestrator.get_summary()
    assert summary["release_blockers"] > 0
    assert summary["overall_health"] == "Blocked"
