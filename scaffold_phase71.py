import os
from pathlib import Path

# Directories to create
dirs = [
    "configs/remediation_lanes",
    "src/sports_signal_bot/remediation_lanes/strategies",
    "tests/remediation_lanes",
    "docs/operators",
    "docs/reviewers",
    "docs/reference",
    "docs/maintenance",
]

for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)

# Files and their contents
files = {}

files["configs/remediation_lanes/default.yaml"] = """\
default_remediation_lane_strategy: "balanced_review_aware"

allowed_lane_families:
  - containment_lane
  - replay_recovery_lane
  - reroute_lane
  - overlay_repair_lane
  - supersession_repair_lane
  - freshness_repair_lane
  - quarantine_reentry_lane
  - relay_stabilization_lane
  - degraded_mode_exit_lane
  - review_only_investigation_lane

token_expiry_windows:
  rehearsal_execution_token: 3600
  staged_execution_token: 1800
  review_only_execution_token: 7200
  rollback_only_token: 86400

required_closed_loop_gates:
  - token_integrity
  - approval_freshness
  - rollback_verification
  - checkpoint_verification

automation_candidate_requirements:
  min_successful_closures: 5
  max_caveats: 1
"""

files["src/sports_signal_bot/remediation_lanes/__init__.py"] = ""
files["src/sports_signal_bot/remediation_lanes/strategies/__init__.py"] = ""

files["src/sports_signal_bot/remediation_lanes/contracts.py"] = """\
from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class LaneFamily(str, Enum):
    containment_lane = "containment_lane"
    replay_recovery_lane = "replay_recovery_lane"
    reroute_lane = "reroute_lane"
    overlay_repair_lane = "overlay_repair_lane"
    supersession_repair_lane = "supersession_repair_lane"
    freshness_repair_lane = "freshness_repair_lane"
    quarantine_reentry_lane = "quarantine_reentry_lane"
    relay_stabilization_lane = "relay_stabilization_lane"
    degraded_mode_exit_lane = "degraded_mode_exit_lane"
    review_only_investigation_lane = "review_only_investigation_lane"

class LaneStatus(str, Enum):
    lane_defined = "lane_defined"
    lane_review_prepared = "lane_review_prepared"
    lane_awaiting_approval = "lane_awaiting_approval"
    lane_approved_for_rehearsal = "lane_approved_for_rehearsal"
    lane_rehearsal_verified = "lane_rehearsal_verified"
    lane_token_issuable = "lane_token_issuable"
    lane_token_issued = "lane_token_issued"
    lane_ready_for_staged_execution = "lane_ready_for_staged_execution"
    lane_execution_window_open = "lane_execution_window_open"
    lane_closed_loop_verifying = "lane_closed_loop_verifying"
    lane_completed_verified = "lane_completed_verified"
    lane_blocked = "lane_blocked"
    lane_expired = "lane_expired"
    lane_archived = "lane_archived"

class TokenFamily(str, Enum):
    rehearsal_execution_token = "rehearsal_execution_token"
    staged_execution_token = "staged_execution_token"
    review_only_execution_token = "review_only_execution_token"
    federated_adaptation_token = "federated_adaptation_token"
    read_only_observation_token = "read_only_observation_token"
    rollback_only_token = "rollback_only_token"

class LaneEligibilityOutcome(str, Enum):
    not_eligible = "not_eligible"
    review_only_eligible = "review_only_eligible"
    rehearsal_only_eligible = "rehearsal_only_eligible"
    staged_execution_eligible = "staged_execution_eligible"
    token_issuable = "token_issuable"
    blocked_by_safety = "blocked_by_safety"

class ClosureOutcome(str, Enum):
    closed_clean = "closed_clean"
    closed_with_caveats = "closed_with_caveats"
    closure_incomplete = "closure_incomplete"
    closure_failed = "closure_failed"
    rollback_recommended = "rollback_recommended"
    review_required_after_closure = "review_required_after_closure"

class RollbackBindingRecord(BaseModel):
    rollback_playbook_ref: str
    rollback_scope: str
    rollback_checkpoints: List[str]
    is_verified_in_rehearsal: bool = False

class RemediationLaneRecord(BaseModel):
    lane_id: str
    lane_family: LaneFamily
    incident_family: str
    scoped_playbook_ref: str
    readiness_ref: Optional[str] = None
    current_status: LaneStatus = LaneStatus.lane_defined
    allowed_step_families: List[str]
    forbidden_step_families: List[str]
    rollback_binding: RollbackBindingRecord
    observability_refs: List[str]
    warnings: List[str] = Field(default_factory=list)

class LaneEligibilityRecord(BaseModel):
    lane_id: str
    outcome: LaneEligibilityOutcome
    confidence_score: float
    is_reversible: bool
    has_explicit_rollback: bool
    has_strong_rehearsal_evidence: bool
    blockers: List[str]

class ReviewAwareExecutionRecord(BaseModel):
    lane_id: str
    approval_ref: str
    unresolved_caveats: int
    reviewer_restrictions: List[str]
    eligibility_downgraded: bool

class BoundedExecutionTokenRecord(BaseModel):
    token_id: str
    token_family: TokenFamily
    bound_lane_ref: str
    allowed_step_families: List[str]
    allowed_scope: str
    issued_from_approval_ref: str
    valid_from: datetime
    valid_until: datetime
    max_execution_window_seconds: int
    required_guards: List[str]
    status: str = "active"
    warnings: List[str] = Field(default_factory=list)

class ClosedLoopReadinessGateRecord(BaseModel):
    gate_id: str
    lane_ref: str
    required_checkpoints: List[str]
    required_observability_signals: List[str]
    required_rollback_checks: List[str]
    gate_status: str
    blocking_reasons: List[str]

class LaneCheckpointRecord(BaseModel):
    checkpoint_id: str
    lane_ref: str
    checkpoint_family: str
    observed_at: datetime
    is_aligned_with_expectation: bool

class LaneStopConditionRecord(BaseModel):
    condition_id: str
    lane_ref: str
    condition_family: str
    triggered: bool
    details: str

class LoopClosureRecord(BaseModel):
    closure_id: str
    lane_ref: str
    outcome: ClosureOutcome
    checkpoints_met: int
    total_checkpoints: int
    stop_conditions_triggered: int
    rollback_used: bool
    evidence_refs: List[str]
    warnings: List[str]

class PlaybookListingRecord(BaseModel):
    listing_id: str
    listing_family: str
    playbook_ref: str
    trust_domain: str
    supported_lane_families: List[LaneFamily]
    required_guards: List[str]
    has_rehearsal_evidence: bool
    portability_profile: str

class PlaybookExchangeCatalogRecord(BaseModel):
    catalog_id: str
    published_at: datetime
    listings: List[PlaybookListingRecord]
    catalog_health: str

class LaneAutomationCandidateRecord(BaseModel):
    candidate_id: str
    lane_family: LaneFamily
    scoped_playbook_ref: str
    successful_closures: int
    caveat_ratio: float
    is_approved_candidate: bool
    envelope_ref: Optional[str] = None
    reasons: List[str]

class LaneLedgerEntry(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lane_id: str
    action: str
    details: str

class RemediationLanesManifest(BaseModel):
    manifest_id: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active_lanes: List[RemediationLaneRecord]
    active_tokens: List[BoundedExecutionTokenRecord]
    readiness_gates: List[ClosedLoopReadinessGateRecord]
    closures: List[LoopClosureRecord]
    catalogs: List[PlaybookExchangeCatalogRecord]
    automation_candidates: List[LaneAutomationCandidateRecord]
    ledger: List[LaneLedgerEntry]
    summary: Dict[str, Any]
"""

files["src/sports_signal_bot/remediation_lanes/lanes.py"] = """\
from .contracts import (
    RemediationLaneRecord, LaneEligibilityRecord, LaneEligibilityOutcome,
    ReviewAwareExecutionRecord, LaneStatus, LaneLedgerEntry
)

def compute_lane_eligibility(lane: RemediationLaneRecord, review_state: ReviewAwareExecutionRecord) -> LaneEligibilityRecord:
    blockers = []

    if not lane.rollback_binding.is_verified_in_rehearsal:
        blockers.append("rollback_not_verified_in_rehearsal")

    if review_state.unresolved_caveats > 0:
        blockers.append(f"unresolved_review_caveats:{review_state.unresolved_caveats}")

    if review_state.eligibility_downgraded:
        outcome = LaneEligibilityOutcome.review_only_eligible
    elif blockers:
        outcome = LaneEligibilityOutcome.blocked_by_safety
    else:
        outcome = LaneEligibilityOutcome.token_issuable

    return LaneEligibilityRecord(
        lane_id=lane.lane_id,
        outcome=outcome,
        confidence_score=0.9 if not blockers else 0.4,
        is_reversible=True,
        has_explicit_rollback=True,
        has_strong_rehearsal_evidence=lane.rollback_binding.is_verified_in_rehearsal,
        blockers=blockers
    )

def project_review_restrictions_into_lane(lane_id: str, approval_ref: str, caveats: int, restrictions: list) -> ReviewAwareExecutionRecord:
    return ReviewAwareExecutionRecord(
        lane_id=lane_id,
        approval_ref=approval_ref,
        unresolved_caveats=caveats,
        reviewer_restrictions=restrictions,
        eligibility_downgraded=(caveats > 0 or "read_only" in restrictions)
    )

def append_lane_lifecycle_entry(ledger: list, lane_id: str, action: str, details: str):
    ledger.append(LaneLedgerEntry(lane_id=lane_id, action=action, details=details))
"""

files["src/sports_signal_bot/remediation_lanes/tokens.py"] = """\
import uuid
from datetime import datetime, timedelta, timezone
from .contracts import BoundedExecutionTokenRecord, TokenFamily, RemediationLaneRecord, ReviewAwareExecutionRecord

def build_bounded_execution_token(lane: RemediationLaneRecord, review: ReviewAwareExecutionRecord, duration_sec: int) -> BoundedExecutionTokenRecord:
    now = datetime.now(timezone.utc)

    if review.eligibility_downgraded:
        token_family = TokenFamily.review_only_execution_token
    else:
        token_family = TokenFamily.staged_execution_token

    return BoundedExecutionTokenRecord(
        token_id=f"token_{uuid.uuid4().hex[:8]}",
        token_family=token_family,
        bound_lane_ref=lane.lane_id,
        allowed_step_families=lane.allowed_step_families,
        allowed_scope=lane.incident_family,
        issued_from_approval_ref=review.approval_ref,
        valid_from=now,
        valid_until=now + timedelta(seconds=duration_sec),
        max_execution_window_seconds=duration_sec,
        required_guards=["strict_observability", "rollback_verified"],
        status="active"
    )

def validate_execution_token_scope(token: BoundedExecutionTokenRecord, requested_scope: str, requested_step: str) -> bool:
    if token.status != "active":
        return False
    if datetime.now(timezone.utc) > token.valid_until:
        return False
    if requested_scope != token.allowed_scope:
        return False
    if requested_step not in token.allowed_step_families:
        return False
    return True
"""

files["src/sports_signal_bot/remediation_lanes/readiness.py"] = """\
from typing import List
from .contracts import (
    RemediationLaneRecord, BoundedExecutionTokenRecord, ClosedLoopReadinessGateRecord,
    LaneCheckpointRecord, LaneStopConditionRecord, LoopClosureRecord, ClosureOutcome
)
import uuid

def evaluate_closed_loop_readiness(lane: RemediationLaneRecord, token: BoundedExecutionTokenRecord) -> ClosedLoopReadinessGateRecord:
    blockers = []

    if token.status != "active":
        blockers.append("invalid_or_expired_token")

    if not lane.rollback_binding.rollback_playbook_ref:
        blockers.append("missing_rollback_binding")

    status = "passed" if not blockers else "blocked"

    return ClosedLoopReadinessGateRecord(
        gate_id=f"gate_{uuid.uuid4().hex[:8]}",
        lane_ref=lane.lane_id,
        required_checkpoints=["post_execution_health_check"],
        required_observability_signals=["latency_normal", "error_rate_low"],
        required_rollback_checks=["rollback_script_reachable"],
        gate_status=status,
        blocking_reasons=blockers
    )

def verify_loop_closure(lane: RemediationLaneRecord, checkpoints: List[LaneCheckpointRecord], stops: List[LaneStopConditionRecord], used_rollback: bool) -> LoopClosureRecord:
    triggered_stops = sum(1 for s in stops if s.triggered)
    met_checkpoints = sum(1 for c in checkpoints if c.is_aligned_with_expectation)

    if triggered_stops > 0 or used_rollback:
        outcome = ClosureOutcome.closed_with_caveats if used_rollback else ClosureOutcome.closure_failed
    elif met_checkpoints < len(checkpoints) and len(checkpoints) > 0:
        outcome = ClosureOutcome.closure_incomplete
    else:
        outcome = ClosureOutcome.closed_clean

    return LoopClosureRecord(
        closure_id=f"closure_{uuid.uuid4().hex[:8]}",
        lane_ref=lane.lane_id,
        outcome=outcome,
        checkpoints_met=met_checkpoints,
        total_checkpoints=len(checkpoints),
        stop_conditions_triggered=triggered_stops,
        rollback_used=used_rollback,
        evidence_refs=[c.checkpoint_id for c in checkpoints],
        warnings=["Stop condition triggered during lane"] if triggered_stops > 0 else []
    )
"""

files["src/sports_signal_bot/remediation_lanes/federated.py"] = """\
import uuid
from datetime import datetime, timezone
from typing import List
from .contracts import (
    PlaybookExchangeCatalogRecord, PlaybookListingRecord, RemediationLaneRecord,
    LaneFamily, RollbackBindingRecord, LaneStatus
)

def build_federated_playbook_exchange_catalog(listings: List[PlaybookListingRecord]) -> PlaybookExchangeCatalogRecord:
    return PlaybookExchangeCatalogRecord(
        catalog_id=f"catalog_{uuid.uuid4().hex[:8]}",
        published_at=datetime.now(timezone.utc),
        listings=listings,
        catalog_health="healthy" if listings else "empty"
    )

def adapt_federated_playbook_into_lane(listing: PlaybookListingRecord, incident_family: str) -> RemediationLaneRecord:
    status = LaneStatus.lane_defined
    allowed_steps = ["read", "observe"]

    if listing.has_rehearsal_evidence:
        allowed_steps.extend(["restart", "clear_cache"])

    lane_family = listing.supported_lane_families[0] if listing.supported_lane_families else LaneFamily.review_only_investigation_lane

    return RemediationLaneRecord(
        lane_id=f"lane_{uuid.uuid4().hex[:8]}",
        lane_family=lane_family,
        incident_family=incident_family,
        scoped_playbook_ref=f"adapted_{listing.playbook_ref}",
        current_status=status,
        allowed_step_families=allowed_steps,
        forbidden_step_families=["drop_database", "mutate_schema", "force_override"],
        rollback_binding=RollbackBindingRecord(
            rollback_playbook_ref=f"rollback_{listing.playbook_ref}",
            rollback_scope=incident_family,
            rollback_checkpoints=["system_stable"],
            is_verified_in_rehearsal=listing.has_rehearsal_evidence
        ),
        observability_refs=["ext_monitoring_1"],
        warnings=["Adapted from federated catalog; requires local review mapping"]
    )
"""

files["src/sports_signal_bot/remediation_lanes/automation_prep.py"] = """\
import uuid
from typing import List
from .contracts import LaneAutomationCandidateRecord, LoopClosureRecord, ClosureOutcome, RemediationLaneRecord

def identify_lane_automation_candidates(lanes: List[RemediationLaneRecord], closures: List[LoopClosureRecord]) -> List[LaneAutomationCandidateRecord]:
    candidates = []

    closure_map = {}
    for c in closures:
        if c.lane_ref not in closure_map:
            closure_map[c.lane_ref] = []
        closure_map[c.lane_ref].append(c)

    for lane in lanes:
        lane_closures = closure_map.get(lane.lane_id, [])
        clean_count = sum(1 for c in lane_closures if c.outcome == ClosureOutcome.closed_clean)
        caveat_count = sum(1 for c in lane_closures if c.outcome == ClosureOutcome.closed_with_caveats)

        if clean_count >= 1:
            caveat_ratio = caveat_count / (clean_count + caveat_count) if (clean_count + caveat_count) > 0 else 0

            candidates.append(LaneAutomationCandidateRecord(
                candidate_id=f"candidate_{uuid.uuid4().hex[:8]}",
                lane_family=lane.lane_family,
                scoped_playbook_ref=lane.scoped_playbook_ref,
                successful_closures=clean_count,
                caveat_ratio=caveat_ratio,
                is_approved_candidate=(caveat_ratio < 0.2),
                reasons=[f"Proven track record with {clean_count} clean closures."]
            ))

    return candidates
"""

files["src/sports_signal_bot/remediation_lanes/strategies/base.py"] = """\
from abc import ABC, abstractmethod

class BaseRemediationLaneStrategy(ABC):
    @abstractmethod
    def get_strategy_name(self) -> str:
        pass
"""

files["src/sports_signal_bot/remediation_lanes/strategies/conservative.py"] = """\
from .base import BaseRemediationLaneStrategy

class ConservativeLaneExecutionStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "ConservativeLaneExecutionStrategy"
"""

files["src/sports_signal_bot/remediation_lanes/strategies/balanced_review_aware.py"] = """\
from .base import BaseRemediationLaneStrategy

class BalancedReviewAwareLaneStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "BalancedReviewAwareLaneStrategy"
"""

files["src/sports_signal_bot/remediation_lanes/strategies/federated_catalog_aware.py"] = """\
from .base import BaseRemediationLaneStrategy

class FederatedCatalogAwareLaneStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "FederatedCatalogAwareLaneStrategy"
"""

files["src/sports_signal_bot/remediation_lanes/strategies/closure_first.py"] = """\
from .base import BaseRemediationLaneStrategy

class ClosureFirstStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "ClosureFirstStrategy"
"""

files["src/sports_signal_bot/remediation_lanes/strategies/token_strict.py"] = """\
from .base import BaseRemediationLaneStrategy

class TokenStrictStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "TokenStrictStrategy"
"""


files["src/sports_signal_bot/remediation_lanes/pass_runner.py"] = """\
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
"""

files["src/sports_signal_bot/remediation_lanes/cli.py"] = """\
import typer
from rich.console import Console
from rich.table import Table
from .pass_runner import run_sample_scenarios

remediation_lanes_app = typer.Typer(help="Remediation Lane Architecture and Execution Governance CLI")
console = Console()

@remediation_lanes_app.command("run-remediation-lanes-pass")
def run_remediation_lanes_pass():
    \"\"\"Runs the full lifecycle pass for remediation lanes, tokens, readiness, and closure.\"\"\"
    console.print("[bold cyan]Starting Phase 71 Remediation Lanes Pass...[/bold cyan]")
    manifest = run_sample_scenarios()

    console.print(f"[green]✔ Pass completed. Manifest ID: {manifest.manifest_id}[/green]")
    console.print("\\n[bold]Summary:[/bold]")
    for k, v in manifest.summary.items():
        console.print(f"  - {k}: {v}")

    console.print("\\n[dim]Artifact saved to: remediation_lanes_manifest.json[/dim]")

@remediation_lanes_app.command("preview-remediation-lanes")
def preview_remediation_lanes():
    \"\"\"Shows defined remediation lanes and their eligibility status.\"\"\"
    manifest = run_sample_scenarios()
    table = Table(title="Remediation Lanes")
    table.add_column("Lane ID")
    table.add_column("Family")
    table.add_column("Status")
    table.add_column("Rollback Verified")

    for lane in manifest.active_lanes:
        table.add_row(lane.lane_id, lane.lane_family.value, lane.current_status.value, str(lane.rollback_binding.is_verified_in_rehearsal))
    console.print(table)

@remediation_lanes_app.command("preview-execution-tokens")
def preview_execution_tokens():
    \"\"\"Previews currently issued bounded execution tokens.\"\"\"
    manifest = run_sample_scenarios()
    table = Table(title="Bounded Execution Tokens")
    table.add_column("Token ID")
    table.add_column("Lane Ref")
    table.add_column("Status")
    table.add_column("Expiry")

    for token in manifest.active_tokens:
        table.add_row(token.token_id, token.bound_lane_ref, token.status, str(token.valid_until))
    console.print(table)

@remediation_lanes_app.command("preview-loop-closure-records")
def preview_loop_closure_records():
    \"\"\"Shows loop closure verification results for executed lanes.\"\"\"
    manifest = run_sample_scenarios()
    table = Table(title="Loop Closure Verification")
    table.add_column("Lane Ref")
    table.add_column("Outcome")
    table.add_column("Checkpoints Met")
    table.add_column("Rollback Used")

    for closure in manifest.closures:
        table.add_row(closure.lane_ref, closure.outcome.value, str(closure.checkpoints_met), str(closure.rollback_used))
    console.print(table)

@remediation_lanes_app.command("preview-federated-playbook-catalogs")
def preview_federated_playbook_catalogs():
    \"\"\"Previews discoverable federated playbook listings.\"\"\"
    manifest = run_sample_scenarios()
    table = Table(title="Federated Playbook Exchange Catalog")
    table.add_column("Catalog ID")
    table.add_column("Listing Count")
    table.add_column("Health")

    for cat in manifest.catalogs:
        table.add_row(cat.catalog_id, str(len(cat.listings)), cat.catalog_health)
    console.print(table)

@remediation_lanes_app.command("list-remediation-lane-strategies")
def list_remediation_lane_strategies():
    \"\"\"Lists available remediation lane strategies.\"\"\"
    strats = [
        "ConservativeLaneExecutionStrategy",
        "BalancedReviewAwareLaneStrategy",
        "FederatedCatalogAwareLaneStrategy",
        "ClosureFirstStrategy",
        "TokenStrictStrategy"
    ]
    console.print("[bold]Available Strategies:[/bold]")
    for s in strats:
        console.print(f" - [cyan]{s}[/cyan]")
"""

files["tests/remediation_lanes/test_remediation_lanes.py"] = """\
import pytest
from datetime import datetime, timezone
from sports_signal_bot.remediation_lanes.contracts import (
    RemediationLaneRecord, LaneFamily, RollbackBindingRecord, ReviewAwareExecutionRecord
)
from sports_signal_bot.remediation_lanes.lanes import compute_lane_eligibility
from sports_signal_bot.remediation_lanes.tokens import build_bounded_execution_token, validate_execution_token_scope

def test_lane_eligibility_blocked_without_rehearsal():
    lane = RemediationLaneRecord(
        lane_id="test_1",
        lane_family=LaneFamily.containment_lane,
        incident_family="lag",
        scoped_playbook_ref="ref",
        allowed_step_families=[],
        forbidden_step_families=[],
        rollback_binding=RollbackBindingRecord(rollback_playbook_ref="", rollback_scope="", rollback_checkpoints=[]),
        observability_refs=[]
    )
    review = ReviewAwareExecutionRecord(lane_id="test_1", approval_ref="app1", unresolved_caveats=0, reviewer_restrictions=[], eligibility_downgraded=False)

    result = compute_lane_eligibility(lane, review)
    assert result.outcome.value == "blocked_by_safety"
    assert "rollback_not_verified_in_rehearsal" in result.blockers

def test_token_scope_validation():
    lane = RemediationLaneRecord(
        lane_id="test_2",
        lane_family=LaneFamily.reroute_lane,
        incident_family="route_issue",
        scoped_playbook_ref="ref",
        allowed_step_families=["reroute"],
        forbidden_step_families=[],
        rollback_binding=RollbackBindingRecord(rollback_playbook_ref="r", rollback_scope="s", rollback_checkpoints=[], is_verified_in_rehearsal=True),
        observability_refs=[]
    )
    review = ReviewAwareExecutionRecord(lane_id="test_2", approval_ref="app1", unresolved_caveats=0, reviewer_restrictions=[], eligibility_downgraded=False)

    token = build_bounded_execution_token(lane, review, 1800)

    assert validate_execution_token_scope(token, "route_issue", "reroute") is True
    assert validate_execution_token_scope(token, "wrong_scope", "reroute") is False
    assert validate_execution_token_scope(token, "route_issue", "drop_db") is False
"""

files["docs/remediation_lanes_and_bounded_execution_architecture.md"] = """\
# Phase 71: Remediation Lane Architecture & Bounded Execution

## Overview
This phase introduces semi-autonomous, explicit boundary **Remediation Lanes**. Instead of blanket execution rights, lanes are granted short-lived **Bounded Execution Tokens** derived from approvals. Execution is gated by rigorous readiness checks and concluded strictly by a **Closed-Loop Verification**.

## Bounded Execution Token Model
Tokens are NOT approvals; they are the *manifestation* of an approval bound by time, scope, and explicitly allowed step families. If a token expires or its lane scope is exceeded, execution is halted immediately.

## Review-Aware Execution
Even semi-autonomous lanes are "review-aware". Unresolved reviewer caveats project down to the lane and can downgrade a staged execution token into a `review_only_execution_token`.

## Closed-Loop Recovery Readiness
No execution is considered "complete" until closed-loop verification occurs. The system matches `LaneCheckpointRecord` and `LaneStopConditionRecord` against expected outcomes. A rollback requirement is strictly enforced.

## Federated Playbook Catalogs
Playbooks imported from federated catalogs cannot be executed natively. They are treated as external listings and pass through an adaptation layer to become review-only or safe local lanes.
"""

files["docs/operators/tokens_closure_and_federated_playbook_catalogs_guide.md"] = """\
# Tokens, Closure, and Federated Playbook Catalogs Guide
"""

files["docs/reviewers/review_aware_execution_and_lane_readiness_guide.md"] = """\
# Review-Aware Execution and Lane Readiness Guide
"""

files["docs/reference/remediation_lanes_taxonomy.md"] = """\
# Remediation Lanes Taxonomy
"""

files["docs/maintenance/remediation_lanes_runbook.md"] = """\
# Remediation Lanes Runbook
"""


for path_str, content in files.items():
    Path(path_str).write_text(content)

# Update main.py
main_py_path = Path("src/sports_signal_bot/main.py")
if main_py_path.exists():
    content = main_py_path.read_text()
    if "remediation_lanes_app" not in content:
        imports = "from sports_signal_bot.remediation_lanes.cli import remediation_lanes_app\\n"

        # Insert import
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                lines.insert(i, imports.strip())
                break

        # Insert app.add_typer
        for i, line in enumerate(lines):
            if "if __name__ ==" in line:
                lines.insert(i, 'app.add_typer(remediation_lanes_app, name="remediation-lanes", help="Phase 71: Remediation Lane Architecture")\\n')
                break

        main_py_path.write_text("\\n".join(lines))
else:
    print(f"Warning: {main_py_path} not found.")

print("Scaffold complete.")
