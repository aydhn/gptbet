import typer
import json
import uuid
from datetime import datetime
from typing import Optional

from .contracts import (
    TournamentRequestRecord,
    TournamentFamily,
    TournamentUniverseRecord,
    TournamentCandidateRecord
)
from ..simulation.contracts import RiskLevel
from .strategies import (
    ConservativeParetoStrategy,
    BalancedMultiObjectiveStrategy,
    AdvisoryDiscoveryStrategy,
    ProviderFocusedTournamentStrategy,
    PolicyFocusedTournamentStrategy
)
from .reporting import build_tournament_summary

app = typer.Typer(help="Phase 44 Batch Candidate Tournament Ops")

def get_strategy(name: str):
    strategies = {
        "conservative": ConservativeParetoStrategy,
        "balanced": BalancedMultiObjectiveStrategy,
        "advisory": AdvisoryDiscoveryStrategy,
        "provider_focused": ProviderFocusedTournamentStrategy,
        "policy_focused": PolicyFocusedTournamentStrategy
    }
    return strategies.get(name, BalancedMultiObjectiveStrategy)()

def _mock_candidates():
    return [
        TournamentCandidateRecord(
            candidate_id="cand_1",
            suggestion_id="sugg_1",
            patch_id="patch_1",
            target_component_family="threshold",
            scope={"sport": "football"},
            risk_level=RiskLevel.LOW,
            support_strength=0.9,
            confidence_band="high",
            estimated_blast_radius=0.1,
            simulation_ref="sim_ref_1"
        ),
        TournamentCandidateRecord(
            candidate_id="cand_2",
            suggestion_id="sugg_2",
            patch_id="patch_2",
            target_component_family="threshold",
            scope={"sport": "football"},
            risk_level=RiskLevel.MEDIUM,
            support_strength=0.7,
            confidence_band="medium",
            estimated_blast_radius=0.3,
            simulation_ref="sim_ref_2"
        ),
        TournamentCandidateRecord(
            candidate_id="cand_3",
            suggestion_id="sugg_3",
            patch_id="patch_3",
            target_component_family="threshold",
            scope={"sport": "football", "market": "O/U"},
            risk_level=RiskLevel.HIGH,
            support_strength=0.4,
            confidence_band="low",
            estimated_blast_radius=0.6,
            simulation_ref="sim_ref_3"
        )
    ]

@app.command()
def run_tournament(
    family: TournamentFamily = typer.Option(TournamentFamily.THRESHOLD_TOURNAMENT, "--family"),
    strategy: str = typer.Option("balanced", "--strategy")
):
    """Runs a batch candidate tournament."""
    typer.echo(f"Starting {family.value} with strategy '{strategy}'")

    universe = TournamentUniverseRecord(
        universe_id=str(uuid.uuid4()),
        replay_window={"start": datetime.utcnow(), "end": datetime.utcnow()},
        target_sports=["football"],
        target_markets=["O/U"],
        baseline_snapshot_id="base_snap_1",
        release_channel_base="main",
        gate_requirements_profile="standard"
    )

    request = TournamentRequestRecord(
        tournament_id=str(uuid.uuid4()),
        tournament_family=family,
        target_component_family="threshold",
        audience_profile="operator",
        candidate_ids=["cand_1", "cand_2", "cand_3"],
        baseline_ref="base_ref_1",
        simulation_mode="comparative_slot_replay",
        comparison_universe=universe,
        selection_policy="default"
    )

    candidates = _mock_candidates()
    strat_impl = get_strategy(strategy)
    manifest = strat_impl.execute(request, candidates)

    summary = build_tournament_summary(manifest)
    typer.echo(json.dumps(summary, indent=2))
    typer.echo(f"Artifact path: results/tournament_{manifest.tournament_id}.json")

@app.command()
def preview_pareto_front(tournament_id: str):
    """Previews the pareto fronts of a tournament."""
    typer.echo(f"Previewing Pareto fronts for tournament {tournament_id}")
    # Mock output
    typer.echo("Front 1: cand_1")
    typer.echo("Front 2: cand_2")
    typer.echo("Front 3: cand_3")

@app.command()
def preview_shortlist(tournament_id: str):
    """Previews the generated candidate shortlists."""
    typer.echo(f"Previewing shortlists for tournament {tournament_id}")
    typer.echo("- Tier 1 (Review Now): cand_1")
    typer.echo("- Tier 2 (Needs Evidence): cand_2")
    typer.echo("- Tier 3 (Exploratory): None")
    typer.echo("- Tier 4 (Reject): cand_3")

@app.command()
def preview_dominance(tournament_id: str):
    """Previews dominance relations for a tournament."""
    typer.echo(f"Previewing dominance relations for tournament {tournament_id}")
    typer.echo("cand_1 dominates cand_2 on metrics: selected_subset_quality_delta")
    typer.echo("cand_1 dominates cand_3 on metrics: selected_subset_quality_delta, support_strength")

@app.command()
def preview_candidate_scorecards(tournament_id: str):
    """Previews candidate scorecards for a tournament."""
    typer.echo(f"Previewing scorecards for tournament {tournament_id}")
    typer.echo("Candidate: cand_1")
    typer.echo("  Gains: selected_subset_quality_delta: 0.45")
    typer.echo("  Risk: LOW")
    typer.echo("  Gate Burden: LOW | Approval Req")

@app.command()
def list_tournament_strategies():
    """Lists available tournament evaluation strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- conservative")
    typer.echo("- balanced (default)")
    typer.echo("- advisory")
    typer.echo("- provider_focused")
    typer.echo("- policy_focused")
