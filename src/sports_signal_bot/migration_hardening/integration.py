from .matrix import build_operational_visibility_matrix, OperationalVisibilityMatrixRow, validate_operational_visibility_row, summarize_operational_visibility_matrix
from typing import Dict, Any, List
from .contracts import (
    LaneFamily, StageFamily, CheckpointFamily,
    DrillFamily, ChainFamily, WarGameFamily
)
from .migration_lanes import (
    build_disaster_migration_lane, MigrationSourceRecord, MigrationTargetRecord,
    MigrationCheckpointRecord, MigrationCutoverRecord, verify_migration_source,
    verify_migration_checkpoint, evaluate_migration_cutover_honesty, summarize_disaster_migration,
    MigrationRollbackRecord
)
from .team_coordination import (
    build_multi_team_coordination_drill, TeamRoleRecord, CoordinationHandoffRecord,
    register_team_role, execute_coordination_handoff, detect_coordination_gaps, summarize_multi_team_coordination
)
from .recovery_chains import (
    build_archival_recovery_chain, RecoveryChainNodeRecord, RecoveryChainEdgeRecord,
    RecoveryChainDependencyRecord, add_recovery_chain_node, add_recovery_chain_edge,
    verify_recovery_chain_integrity, summarize_archival_recovery_chain
)
from .visibility_wargames import (
    build_governance_visibility_war_game, WarGameVisibilitySurfaceRecord, WarGameSignalRecord,
    inject_visibility_stress, detect_visibility_losses, summarize_visibility_war_game
)
from .strategies.conservative import ConservativeMigrationHardeningStrategy
from datetime import datetime, timezone

class MigrationHardeningOrchestrator:
    def __init__(self):
        self.strategy = ConservativeMigrationHardeningStrategy()
        self.lanes = []
        self.drills = []
        self.chains = []
        self.games = []
        self.matrix = build_operational_visibility_matrix('matrix_001')

    def simulate_archive_to_runtime_migration(self):
        # 1. Lane
        lane = build_disaster_migration_lane("lane_001", LaneFamily.archive_to_runtime_recovery_lane)
        source = MigrationSourceRecord(source_id="src_archive_01", freshness_timestamp=datetime.now(timezone.utc), is_stale=False)
        verify_migration_source(lane, source)

        chk = MigrationCheckpointRecord(checkpoint_id="chk_fresh_01", family=CheckpointFamily.source_freshness_verified_checkpoint, verified=True)
        verify_migration_checkpoint(lane, chk)

        rb = MigrationRollbackRecord(rollback_id="rb_01", is_explicit=True)
        lane.rollback_refs.append(rb)

        cutover = MigrationCutoverRecord(cutover_id="cut_01")
        evaluate_migration_cutover_honesty(lane, cutover)

        self.lanes.append(lane)

    def simulate_cross_team_no_safe_handoff(self):
        # 2. Drill
        drill = build_multi_team_coordination_drill("drill_001", DrillFamily.operator_reviewer_coordination_drill)
        r1 = TeamRoleRecord(role_id="r1", role_family="local_operator", owner="Alice")
        r2 = TeamRoleRecord(role_id="r2", role_family="governance_owner", owner="Bob")
        register_team_role(drill, r1)
        register_team_role(drill, r2)

        h1 = CoordinationHandoffRecord(handoff_id="h1", from_role="r1", to_role="r2", details="Handoff no_safe state", is_acknowledged=True, freshness_note_preserved=True)
        execute_coordination_handoff(drill, h1)
        detect_coordination_gaps(drill)

        self.drills.append(drill)

    def simulate_broken_recovery_chain(self):
        # 3. Chain
        chain = build_archival_recovery_chain("chain_001", ChainFamily.archive_restore_chain)
        n1 = RecoveryChainNodeRecord(node_id="n1", description="Archive Base")
        n2 = RecoveryChainNodeRecord(node_id="n2", description="Restored State")
        add_recovery_chain_node(chain, n1)
        add_recovery_chain_node(chain, n2)

        e1 = RecoveryChainEdgeRecord(edge_id="e1", from_node="n1", to_node="n2", has_lineage=False) # Broken lineage
        add_recovery_chain_edge(chain, e1)

        dep = RecoveryChainDependencyRecord(dependency_id="dep1", is_broken=True)
        chain.dependency_refs.append(dep)

        verify_recovery_chain_integrity(chain)
        self.chains.append(chain)

    def populate_visibility_matrix(self):
        row = OperationalVisibilityMatrixRow(row_id="r1", surface_name="migration lanes", owner_visible=True, no_safe_visible=True, sovereignty_note_visible=True)
        validate_operational_visibility_row(self.matrix, row)

    def simulate_executive_visibility_honesty(self):
        # 4. WarGame
        game = build_governance_visibility_war_game("game_001", WarGameFamily.executive_summary_visibility_war_game)
        surf = WarGameVisibilitySurfaceRecord(surface_id="surf_01", maintains_no_safe=False, maintains_sovereignty=True) # Loss injected
        sig = WarGameSignalRecord(signal_id="sig_01", is_suppressed=True)

        inject_visibility_stress(game, surf, sig)
        detect_visibility_losses(game)

        self.games.append(game)


    def simulate_stale_source_migration_rejection(self):
        lane = build_disaster_migration_lane("lane_002", LaneFamily.archive_to_archive_migration_lane)
        source = MigrationSourceRecord(source_id="src_stale_01", freshness_timestamp=datetime.now(), is_stale=True)
        verify_migration_source(lane, source)
        self.lanes.append(lane)

    def simulate_mixed_disaster_migration_and_rollback(self):
        lane = build_disaster_migration_lane("lane_003", LaneFamily.mixed_disaster_migration_lane)
        source = MigrationSourceRecord(source_id="src_mixed_01", freshness_timestamp=datetime.now(), is_stale=False)
        verify_migration_source(lane, source)
        rb = MigrationRollbackRecord(rollback_id="rb_mixed_01", is_explicit=True)
        lane.rollback_refs.append(rb)
        cutover = MigrationCutoverRecord(cutover_id="cut_03")
        evaluate_migration_cutover_honesty(lane, cutover)
        self.lanes.append(lane)

    def simulate_sovereignty_continuity_disaster_handoff(self):
        drill = build_multi_team_coordination_drill("drill_002", DrillFamily.sovereignty_visibility_coordination_drill)
        self.drills.append(drill)

    def simulate_queue_pressure_coordination(self):
        drill = build_multi_team_coordination_drill("drill_003", DrillFamily.mixed_team_handoff_drill)
        self.drills.append(drill)

    def simulate_residue_heavy_coordination(self):
        drill = build_multi_team_coordination_drill("drill_004", DrillFamily.mixed_team_handoff_drill)
        self.drills.append(drill)

    def simulate_archive_continuity_visibility_combined(self):
        game = build_governance_visibility_war_game("game_002", WarGameFamily.archive_visibility_war_game)
        self.games.append(game)

    def run_all_simulations(self):
        self.simulate_archive_to_runtime_migration()
        self.simulate_cross_team_no_safe_handoff()
        self.simulate_broken_recovery_chain()
        self.simulate_executive_visibility_honesty()
        self.simulate_stale_source_migration_rejection()
        self.simulate_mixed_disaster_migration_and_rollback()
        self.simulate_sovereignty_continuity_disaster_handoff()
        self.simulate_queue_pressure_coordination()
        self.simulate_residue_heavy_coordination()
        self.simulate_archive_continuity_visibility_combined()
        self.populate_visibility_matrix()

    def get_summary(self):
        lane_summaries = [summarize_disaster_migration(l) for l in self.lanes]
        drill_summaries = [summarize_multi_team_coordination(d) for d in self.drills]
        chain_summaries = [summarize_archival_recovery_chain(c) for c in self.chains]
        game_summaries = [summarize_visibility_war_game(g) for g in self.games]
        matrix_summary = summarize_operational_visibility_matrix(self.matrix)

        release_blockers = 0
        for l in self.lanes:
            if self.strategy.evaluate_migration_readiness({'lane': l}).get('is_release_blocking'): release_blockers += 1
        for d in self.drills:
             if self.strategy.evaluate_coordination({'drill': d}).get('is_release_blocking'): release_blockers += 1
        for c in self.chains:
             if self.strategy.evaluate_recovery_chain({'chain': c}).get('is_release_blocking'): release_blockers += 1
        for g in self.games:
             if self.strategy.evaluate_visibility_wargame({'game': g}).get('is_release_blocking'): release_blockers += 1

        return {
            "migration_lanes": lane_summaries,
            "coordination_drills": drill_summaries,
            "recovery_chains": chain_summaries,
            "visibility_wargames": game_summaries,
            "visibility_matrix": matrix_summary,
            "release_blockers": release_blockers,
            "overall_health": "Blocked" if release_blockers > 0 else "Verified"
        }
