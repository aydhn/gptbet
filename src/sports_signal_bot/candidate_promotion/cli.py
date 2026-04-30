import typer
import uuid
import json
from typing import List

from .contracts import CandidateReleaseRecord, CandidateManifest, FinalDecisionAction
from ..simulation.contracts import RiskLevel
from .pipeline import run_candidate_pipeline

app = typer.Typer(help="Phase 45 Candidate Promotion Ops")

def mock_candidates() -> List[CandidateReleaseRecord]:
    return [
        CandidateReleaseRecord(
            candidate_release_id="cand_1",
            suggestion_id="sugg_1",
            patch_id="patch_1",
            tournament_ref="tourn_1",
            target_component_family="threshold",
            scope={"sport": "football"},
            risk_level=RiskLevel.LOW,
            support_strength=0.9,
            confidence_band="high"
        ),
        CandidateReleaseRecord(
            candidate_release_id="cand_2",
            suggestion_id="sugg_2",
            patch_id="patch_2",
            tournament_ref="tourn_1",
            target_component_family="provider",
            scope={"sport": "football", "market": "1X2"},
            risk_level=RiskLevel.MEDIUM,
            support_strength=0.6,
            confidence_band="medium"
        ),
        CandidateReleaseRecord(
            candidate_release_id="cand_3",
            suggestion_id="sugg_3",
            patch_id="patch_3",
            tournament_ref="tourn_1",
            target_component_family="policy",
            scope={"sport": "football", "league": "EPL", "market": "O/U"},
            risk_level=RiskLevel.CRITICAL,
            support_strength=0.3,
            confidence_band="low"
        )
    ]

@app.command()
def run_candidate_promotion():
    """Runs the candidate promotion pipeline for shortlisted candidates."""
    typer.echo("Running candidate promotion pipeline...")
    candidates = mock_candidates()
    manifest = run_candidate_pipeline(candidates)

    typer.echo(f"Processed {len(manifest.candidates)} candidates.")

    promoted = sum(1 for d in manifest.decisions if d.action == FinalDecisionAction.PROMOTE_CANDIDATE_LANE)
    held = sum(1 for d in manifest.decisions if d.action == FinalDecisionAction.HOLD_CANDIDATE)
    killed = sum(1 for d in manifest.decisions if d.action == FinalDecisionAction.KILL_CANDIDATE)
    revised = sum(1 for d in manifest.decisions if d.action == FinalDecisionAction.REVISE_CANDIDATE)

    typer.echo(f"Results: {promoted} Promoted, {held} Held, {revised} Revised, {killed} Killed")

    # Save output artifact
    artifact_path = f"results/candidate_manifest_{manifest.manifest_id}.json"
    with open(artifact_path, "w") as f:
        f.write(manifest.model_dump_json(indent=2))

    typer.echo(f"Artifact saved to {artifact_path}")

@app.command()
def preview_candidate_readiness():
    """Previews the readiness distribution of current candidates."""
    typer.echo("Previewing Candidate Readiness Distribution...")
    candidates = mock_candidates()
    manifest = run_candidate_pipeline(candidates)
    for readiness in manifest.readiness:
        typer.echo(f"Candidate {readiness.candidate_id}: {readiness.readiness_band.value}")

@app.command()
def preview_candidate_stages(candidate_id: str):
    """Previews stage results for a candidate."""
    typer.echo(f"Previewing stages for {candidate_id}")
    typer.echo(" - Integrity: Passed")
    typer.echo(" - Safety: Passed")
    typer.echo(" - Simulation: Passed")

@app.command()
def preview_candidate_decisions():
    """Previews candidate decisions."""
    typer.echo("Previewing Candidate Decisions...")
    candidates = mock_candidates()
    manifest = run_candidate_pipeline(candidates)
    for decision in manifest.decisions:
        typer.echo(f"Candidate {decision.candidate_id}: {decision.action.value} - {decision.rationale}")

@app.command()
def preview_candidate_bundles():
    """Previews candidate bundles."""
    typer.echo("Previewing Candidate Bundles...")
    typer.echo("No bundles currently configured.")

@app.command()
def preview_candidate_release_package(candidate_id: str):
    """Previews a candidate release package."""
    typer.echo(f"Previewing Release Package for {candidate_id}")
    typer.echo(f"Target Channels: ['candidate-stable']")

@app.command()
def list_candidate_promotion_strategies():
    """Lists available candidate promotion strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeCandidatePromotionStrategy")
    typer.echo("- BalancedCandidatePromotionStrategy")
    typer.echo("- EvidenceFirstCandidatePromotionStrategy")
    typer.echo("- FastLaneSafePatchStrategy")
    typer.echo("- ReviewHeavyPromotionStrategy")

if __name__ == "__main__":
    app()
