import uuid
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from .contracts import (
    LaneFamily, RollbackBindingRecord, RemediationLaneRecord, LaneCheckpointRecord, LaneStopConditionRecord,
    PlaybookListingRecord, RemediationLanesManifest, ClosureOutcome, TokenFamily
)
from .lanes import compute_lane_eligibility, project_review_restrictions_into_lane, append_lane_lifecycle_entry
from .tokens import build_bounded_execution_token
from .readiness import evaluate_closed_loop_readiness, verify_loop_closure
from .federated import build_federated_playbook_exchange_catalog, adapt_federated_playbook_into_lane
from .automation_prep import identify_lane_automation_candidates

def run_sample_scenarios() -> RemediationLanesManifest:
    ledger = []
    active_lanes = []
    active_tokens = []
    gates = []
    closures = []

    # Scenario 1
    lane1 = RemediationLaneRecord(
        lane_id=f"lane_{uuid.uuid4().hex[:8]}",
        lane_family=LaneFamily.replay_recovery_lane,
        incident_family="backlog_spike",
        scoped_playbook_ref="pb_replay_flush",
        allowed_step_families=["flush_queue", "restart_worker"],
        forbidden_step_families=["drop_queue"],
        rollback_binding=RollbackBindingRecord(
            rollback_playbook_ref="rb_replay_stop",
            rollback_scope="backlog_spike",
            rollback_checkpoints=[],
            is_verified_in_rehearsal=True
        ),
        observability_refs=["queue_depth_metric"]
    )
    active_lanes.append(lane1)
    append_lane_lifecycle_entry(ledger, lane1.lane_id, "lane_defined", "Backlog lane defined.")

    review1 = project_review_restrictions_into_lane(lane1.lane_id, "app_001", 0, [])
    eligibility1 = compute_lane_eligibility(lane1, review1)

    if eligibility1.outcome.value in ["token_issuable", "staged_execution_eligible"]:
        token1 = build_bounded_execution_token(lane1, review1, 1800)
        active_tokens.append(token1)
        append_lane_lifecycle_entry(ledger, lane1.lane_id, "token_issued", f"Token {token1.token_id} issued.")

        gate1 = evaluate_closed_loop_readiness(lane1, token1)
        gates.append(gate1)

        checks1 = [LaneCheckpointRecord(checkpoint_id="chk_1", lane_ref=lane1.lane_id, checkpoint_family="queue_cleared", observed_at=datetime.now(timezone.utc), is_aligned_with_expectation=True)]
        closure1 = verify_loop_closure(lane1, checks1, [], used_rollback=False)
        closures.append(closure1)
        append_lane_lifecycle_entry(ledger, lane1.lane_id, "closure_verified", "Lane cleanly closed.")

    # Scenario 2
    listing = PlaybookListingRecord(
        listing_id="list_001",
        listing_family="federated_playbook_listing",
        playbook_ref="fed_sync_repair",
        trust_domain="external_partner",
        supported_lane_families=[LaneFamily.containment_lane],
        required_guards=["safe_mode"],
        has_rehearsal_evidence=False,
        portability_profile="generic_v1"
    )
    catalog = build_federated_playbook_exchange_catalog([listing])

    lane2 = adapt_federated_playbook_into_lane(listing, "external_sync_issue")
    active_lanes.append(lane2)
    append_lane_lifecycle_entry(ledger, lane2.lane_id, "federated_adaptation", "Imported and adapted playbook as review-only lane.")

    # Scenario 3
    lane3 = RemediationLaneRecord(
        lane_id=f"lane_{uuid.uuid4().hex[:8]}",
        lane_family=LaneFamily.containment_lane,
        incident_family="sync_lag",
        scoped_playbook_ref="pb_sync_pause",
        allowed_step_families=["pause_sync"],
        forbidden_step_families=["force_sync"],
        rollback_binding=RollbackBindingRecord(rollback_playbook_ref="", rollback_scope="", rollback_checkpoints=[], is_verified_in_rehearsal=False),
        observability_refs=["lag_metric"],
        warnings=["Missing stop condition coverage"]
    )
    active_lanes.append(lane3)
    review3 = project_review_restrictions_into_lane(lane3.lane_id, "app_003", 0, [])
    eligibility3 = compute_lane_eligibility(lane3, review3)
    append_lane_lifecycle_entry(ledger, lane3.lane_id, "eligibility_blocked", f"Blockers: {eligibility3.blockers}")

    # Scenario 4
    lane4 = RemediationLaneRecord(
        lane_id=f"lane_{uuid.uuid4().hex[:8]}",
        lane_family=LaneFamily.degraded_mode_exit_lane,
        incident_family="api_degraded",
        scoped_playbook_ref="pb_exit_degraded",
        allowed_step_families=["resume_traffic"],
        forbidden_step_families=[],
        rollback_binding=RollbackBindingRecord(rollback_playbook_ref="rb_degraded", rollback_scope="api_degraded", rollback_checkpoints=[], is_verified_in_rehearsal=True),
        observability_refs=[]
    )
    active_lanes.append(lane4)
    review4 = project_review_restrictions_into_lane(lane4.lane_id, "app_004", 0, [])
    token4 = build_bounded_execution_token(lane4, review4, 1800)
    token4.valid_until = datetime.now(timezone.utc)
    token4.status = "expired"
    active_tokens.append(token4)
    append_lane_lifecycle_entry(ledger, lane4.lane_id, "token_expired", "Token expired before execution.")

    # Scenario 5
    lane5 = RemediationLaneRecord(
        lane_id=f"lane_{uuid.uuid4().hex[:8]}",
        lane_family=LaneFamily.supersession_repair_lane,
        incident_family="stale_data",
        scoped_playbook_ref="pb_supersede",
        allowed_step_families=["write_overlay"],
        forbidden_step_families=[],
        rollback_binding=RollbackBindingRecord(rollback_playbook_ref="rb_overlay", rollback_scope="stale_data", rollback_checkpoints=[], is_verified_in_rehearsal=True),
        observability_refs=[]
    )
    active_lanes.append(lane5)
    review5 = project_review_restrictions_into_lane(lane5.lane_id, "app_005", 0, [])
    token5 = build_bounded_execution_token(lane5, review5, 1800)
    active_tokens.append(token5)

    stop_cond = LaneStopConditionRecord(condition_id="stop_1", lane_ref=lane5.lane_id, condition_family="observability_gap", triggered=True, details="Observability signal degraded.")
    closure5 = verify_loop_closure(lane5, [], [stop_cond], used_rollback=False)
    closures.append(closure5)
    append_lane_lifecycle_entry(ledger, lane5.lane_id, "closure_with_caveats", "Lane closed but triggered stop conditions.")

    candidates = identify_lane_automation_candidates(active_lanes, closures)

    summary = {
        "lane_count": len(active_lanes),
        "token_issued_count": len(active_tokens),
        "closures_clean": sum(1 for c in closures if c.outcome == ClosureOutcome.closed_clean),
        "closures_caveated": sum(1 for c in closures if c.outcome == ClosureOutcome.closed_with_caveats),
        "federated_catalogs_count": 1,
        "automation_candidates_count": len(candidates)
    }

    manifest = RemediationLanesManifest(
        manifest_id=f"mani_{uuid.uuid4().hex[:8]}",
        active_lanes=active_lanes,
        active_tokens=active_tokens,
        readiness_gates=gates,
        closures=closures,
        catalogs=[catalog],
        automation_candidates=candidates,
        ledger=ledger,
        summary=summary
    )

    output_path = Path("remediation_lanes_manifest.json")
    output_path.write_text(manifest.model_dump_json(indent=2))

    return manifest
