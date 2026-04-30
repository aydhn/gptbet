import typer
import yaml
import os
import datetime
import uuid
from typing import List, Dict, Any
from .contracts import (
    ChannelFamily, StageStatus, CandidateChannelRecord,
    RolloutStageRecord, CandidateFleetRecord, RolloutDecisionRecord, NextStepReadinessRecord
)
from .channels import resolve_channel_evaluation_profile
from .progression import simulate_rollout_stage, compute_next_step_readiness
from .fleets import detect_fleet_conflicts, build_candidate_fleet
from .manifests import write_manifest
from .strategies.balanced_phased import BalancedPhasedRolloutStrategy

app = typer.Typer(help="Staged Candidate Channels (Phase 46)")

# Mock datastore for sample flows
def get_mock_state():
    return {
        "channels": [
            CandidateChannelRecord(
                channel_id="shadow_1", channel_name="shadow_candidate_channel",
                channel_family=ChannelFamily.SHADOW_CANDIDATE, safety_level="low",
                comparison_mode="same-universe", progression_policy="default",
                capacity_limits={"max_active": 20}, active_assignments=["cand_narrow_low_risk", "cand_broader_patch"]
            ),
            CandidateChannelRecord(
                channel_id="eval_1", channel_name="candidate_eval_channel",
                channel_family=ChannelFamily.CANDIDATE_EVAL, safety_level="medium",
                comparison_mode="comparative", progression_policy="default",
                capacity_limits={"max_active": 10}, active_assignments=["cand_medium_risk", "cand_conflict_1"]
            ),
            CandidateChannelRecord(
                channel_id="safe_1", channel_name="live_like_safe_channel",
                channel_family=ChannelFamily.LIVE_LIKE_SAFE, safety_level="high",
                comparison_mode="stable-reference", progression_policy="default",
                capacity_limits={"max_active": 5}, active_assignments=[]
            )
        ],
        "stages": [
            RolloutStageRecord(
                stage_id="s1", candidate_release_id="cand_narrow_low_risk", current_channel="shadow_candidate_channel",
                stage_status=StageStatus.SHADOW_VERIFIED, entered_at=datetime.datetime.now(datetime.timezone.utc)
            ),
            RolloutStageRecord(
                stage_id="s2", candidate_release_id="cand_broader_patch", current_channel="shadow_candidate_channel",
                stage_status=StageStatus.RUNNING_IN_SHADOW, entered_at=datetime.datetime.now(datetime.timezone.utc)
            ),
            RolloutStageRecord(
                stage_id="s3", candidate_release_id="cand_medium_risk", current_channel="candidate_eval_channel",
                stage_status=StageStatus.RUNNING_CANDIDATE_EVAL, entered_at=datetime.datetime.now(datetime.timezone.utc)
            ),
            RolloutStageRecord(
                stage_id="s4", candidate_release_id="cand_conflict_1", current_channel="candidate_eval_channel",
                stage_status=StageStatus.RUNNING_CANDIDATE_EVAL, entered_at=datetime.datetime.now(datetime.timezone.utc)
            )
        ],
        "metadata": {
            "cand_medium_risk": {"target_family": "provider_priority"},
            "cand_conflict_1": {"target_family": "provider_priority"}
        }
    }

def load_config() -> Dict[str, Any]:
    config_path = "configs/staged_channels/default.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

@app.command("preview-channel-state")
def preview_channel_state():
    """Preview active candidates by channel."""
    state = get_mock_state()
    config = load_config()
    typer.echo(f"Using Strategy: {config.get('default_channel_strategy', 'Default')}")
    typer.echo("\nActive Channels:")
    for ch in state["channels"]:
        typer.echo(f"- {ch.channel_name}: {len(ch.active_assignments)} candidates ({', '.join(ch.active_assignments) if ch.active_assignments else 'none'})")

@app.command("run-staged-rollout")
def run_staged_rollout():
    """Run staged rollout progression cycle based on sample flows."""
    typer.echo("Running staged rollout progression...")
    state = get_mock_state()
    config = load_config()
    decisions = []

    fleet = build_candidate_fleet(["cand_medium_risk", "cand_conflict_1"], "Eval Fleet")

    for stage_record in state["stages"]:
        cand_id = stage_record.candidate_release_id
        current_status = stage_record.stage_status

        # Strategy lookup based on config is mock here, running standard balanced rules
        strategy = BalancedPhasedRolloutStrategy()

        # 1. narrow low-risk threshold candidate progressing shadow -> candidate_eval -> live_like_safe
        if cand_id == "cand_narrow_low_risk":
            next_status = simulate_rollout_stage(cand_id, current_status)
            typer.echo(f"Evaluating {cand_id} in {current_status.value} -> Promoted to {next_status.value}")
            decisions.append({"candidate": cand_id, "action": "progress", "to": next_status.value})

        # 2. broader candidate rolled back to shadow after stage regression
        elif cand_id == "cand_broader_patch":
            # Simulate regression detected
            next_status = StageStatus.ROLLBACK_TO_SHADOW
            typer.echo(f"Evaluating {cand_id} in {current_status.value} -> Regression detected! {next_status.value}")
            decisions.append({"candidate": cand_id, "action": "rollback", "to": next_status.value})

        # 3. medium-risk provider patch held in candidate_eval due to fleet conflict
        elif cand_id == "cand_medium_risk" or cand_id == "cand_conflict_1":
            conflicts = detect_fleet_conflicts(fleet, state["metadata"])
            if conflicts and not strategy.handle_fleet_conflicts(fleet, cand_id):
                next_status = StageStatus.ROLLOUT_HOLD
                typer.echo(f"Evaluating {cand_id} in {current_status.value} -> Fleet conflict detected ({conflicts[0].description})! Held in {next_status.value}")
                decisions.append({"candidate": cand_id, "action": "hold", "to": next_status.value})

    # Output artifacts
    os.makedirs("artifacts", exist_ok=True)
    write_manifest("artifacts/staged_channel_decisions.json", decisions)
    typer.echo("\nStaged channel manifest updated: artifacts/staged_channel_decisions.json")

@app.command("list-staged-channel-strategies")
def list_staged_channel_strategies():
    """List available channel strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeStagedChannelStrategy")
    typer.echo("- BalancedPhasedRolloutStrategy")
    typer.echo("- FastSafeCandidateWaveStrategy")
    typer.echo("- FleetAwareConflictHeavyStrategy")
    typer.echo("- ReviewWeightedStageStrategy")

@app.command("preview-next-step-readiness")
def preview_next_step_readiness():
    """Show the readiness states of current candidates."""
    typer.echo("Candidate Readiness:")
    state = get_mock_state()
    for stage_record in state["stages"]:
        readiness = compute_next_step_readiness(stage_record.stage_status, stage_record.candidate_release_id)
        typer.echo(f"{readiness.candidate_release_id} -> {readiness.readiness_level}")
