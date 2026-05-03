import typer
import json
import os
from datetime import datetime
from sports_signal_bot.corridor_governance.contracts import (
    CorridorCatalogEntryRecord,
    CorridorCatalogRecord,
    TreatyLifecycleStateRecord,
    TreatyLifecycleControllerRecord,
    SovereignInteroperabilityScorecardRecord,
    ContinuityAttestationRecord
)
from sports_signal_bot.corridor_governance.catalogs import build_corridor_catalog, summarize_corridor_catalog_health
from sports_signal_bot.corridor_governance.treaty_lifecycle import build_treaty_lifecycle_controller, summarize_treaty_lifecycle
from sports_signal_bot.corridor_governance.attestations import summarize_attestation_state
from sports_signal_bot.corridor_governance.strategies.balanced_continuity_attestation import BalancedContinuityAttestationStrategy

app = typer.Typer()

@app.command("run-corridor-governance-pass")
def run_corridor_governance_pass():
    typer.echo("Running corridor governance pass...")

    # Mock data for demonstration
    entry = CorridorCatalogEntryRecord(
        catalog_entry_id="cat-1", corridor_ref="corr-1", source_region_ref="eu-west", target_region_ref="us-east",
        treaty_ref="treaty-1", allowed_lane_families=["review_only"], allowed_transfer_classes=["minimal"],
        continuity_requirement_summary="strict", translation_requirement_summary="standard",
        sovereignty_notes="allowed", freshness_state="current", supersession_state="active",
        visibility_profile="discoverable_internal", warnings=[]
    )
    catalog = build_corridor_catalog([entry])

    treaty_state = TreatyLifecycleStateRecord(
        treaty_ref="treaty-1", lifecycle_state="treaty_active", effective_from=datetime.now(),
        warnings=[]
    )
    lifecycle_controller = build_treaty_lifecycle_controller([treaty_state])

    attestation = ContinuityAttestationRecord(
        continuity_attestation_id="att-1", continuity_session_ref="sess-1", corridor_ref="corr-1",
        treaty_ref="treaty-1", source_region_ref="eu-west", target_region_ref="us-east",
        attestation_family="readiness_continuity_attestation", attested_dimensions=["entry_guard_integrity"],
        attestation_status="attested_verified", validity_window={"effective_from": str(datetime.now())},
        caveat_refs=[], evidence_refs=[], warnings=[]
    )

    scorecard = SovereignInteroperabilityScorecardRecord(
        scorecard_id="score-1", scored_scope="corridor", scored_corridor_refs=["corr-1"],
        scored_treaty_refs=["treaty-1"], region_pair_ref="eu-us", dimension_scores={"corridor_freshness": 95.0},
        overall_score=95.0, overall_band="high_confidence_interop", caveat_summary=[], blocking_gaps=[], warnings=[]
    )

    strategy = BalancedContinuityAttestationStrategy()

    summary = {
        "catalog_health": summarize_corridor_catalog_health(catalog),
        "attestation_state": summarize_attestation_state([attestation]),
        "treaty_lifecycle": summarize_treaty_lifecycle(lifecycle_controller),
        "scorecard_summary": {scorecard.overall_band: 1},
        "strategy": strategy.get_strategy_name(),
        "status": "completed"
    }

    os.makedirs("results", exist_ok=True)
    with open("results/corridor_governance_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    typer.echo("Corridor governance pass complete. Summary written to results/corridor_governance_summary.json.")

@app.command("preview-corridor-catalogs")
def preview_corridor_catalogs():
    typer.echo("Previewing corridor catalogs...")
    typer.echo("  - cat-1: corr-1 (eu-west -> us-east) [visibility: discoverable_internal]")

@app.command("preview-continuity-attestations")
def preview_continuity_attestations():
    typer.echo("Previewing continuity attestations...")
    typer.echo("  - att-1: attested_verified [dimensions: 1]")

@app.command("preview-treaty-lifecycle")
def preview_treaty_lifecycle():
    typer.echo("Previewing treaty lifecycles...")
    typer.echo("  - treaty-1: treaty_active")

@app.command("preview-interoperability-scorecards")
def preview_interoperability_scorecards():
    typer.echo("Previewing interoperability scorecards...")
    typer.echo("  - score-1: high_confidence_interop (95.0)")

@app.command("preview-catalog-suppressions")
def preview_catalog_suppressions():
    typer.echo("Previewing catalog suppressions...")
    typer.echo("  No suppressions currently active.")

@app.command("list-corridor-governance-strategies")
def list_corridor_governance_strategies():
    typer.echo("Available Corridor Governance Strategies:")
    typer.echo("  - ConservativeCorridorCatalogStrategy")
    typer.echo("  - BalancedContinuityAttestationStrategy")
    typer.echo("  - TreatyLifecycleFirstStrategy")
    typer.echo("  - ScorecardStrictStrategy")
    typer.echo("  - SovereigntyDominantCatalogStrategy")
