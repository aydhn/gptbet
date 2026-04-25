import typer
from typing import Optional, List
import yaml
from pathlib import Path
from pydantic import BaseModel
import sys

# Assume sports_signal_bot is in sys.path or run from repo root
try:
    from sports_signal_bot.dynamic_weighting.runner import DynamicWeightingRunner
    from sports_signal_bot.dynamic_weighting.contracts import WeightingManifest, WeightingDecisionRecord
    from sports_signal_bot.dynamic_weighting.manifests import save_weighting_manifest
    from sports_signal_bot.dynamic_weighting.registry import weighting_registry
except ImportError:
    # Adjust for testing context if needed
    from sports_signal_bot.dynamic_weighting.runner import DynamicWeightingRunner
    from sports_signal_bot.dynamic_weighting.contracts import WeightingManifest, WeightingDecisionRecord
    from sports_signal_bot.dynamic_weighting.manifests import save_weighting_manifest
    from sports_signal_bot.dynamic_weighting.registry import weighting_registry


app = typer.Typer(help="Dynamic Weighting Engine CLI")

def _load_yaml(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def _get_mock_eligible_sources(sport: str, market: str) -> List[dict]:
    # Mock data based on the requested sample flows
    if sport == "football" and market == "1x2":
        return [
            {"name": "poisson_1", "family": "probabilistic", "trust_score": 0.8, "regime_fit": 0.9, "regime_sample_size": 100, "probability": 0.45, "is_stale": False, "is_calibrated": False},
            {"name": "elo_1", "family": "benchmark", "trust_score": 0.6, "regime_fit": 0.5, "regime_sample_size": 20, "probability": 0.40, "is_stale": True, "is_calibrated": False},
            {"name": "log_reg_1", "family": "ml_calibrated", "trust_score": 0.9, "regime_fit": 0.8, "regime_sample_size": 200, "probability": 0.48, "is_stale": False, "is_calibrated": True},
        ]
    elif sport == "football" and market == "ou_2_5":
         return [
            {"name": "bookmaker_1", "family": "benchmark", "trust_score": 0.95, "regime_fit": 0.95, "regime_sample_size": 1000, "probability": 0.55, "is_stale": False, "is_calibrated": False},
            {"name": "rf_cal_1", "family": "ml_calibrated", "trust_score": 0.85, "regime_fit": 0.8, "regime_sample_size": 150, "probability": 0.60, "is_stale": False, "is_calibrated": True},
            {"name": "total_prob_1", "family": "probabilistic", "trust_score": 0.7, "regime_fit": 0.6, "regime_sample_size": 50, "probability": 0.45, "is_stale": False, "is_calibrated": False},
        ]
    elif sport == "basketball" and market == "moneyline":
         return [
            {"name": "elo_bb", "family": "elo", "trust_score": 0.8, "regime_fit": 0.8, "regime_sample_size": 500, "probability": 0.70, "is_stale": False, "is_calibrated": False},
            {"name": "struct_bb", "family": "structural", "trust_score": 0.85, "regime_fit": 0.9, "regime_sample_size": 300, "probability": 0.72, "is_stale": False, "is_calibrated": False},
            {"name": "gb_cal_1", "family": "ml_calibrated", "trust_score": 0.9, "regime_fit": 0.85, "regime_sample_size": 400, "probability": 0.68, "is_stale": False, "is_calibrated": True},
        ]
    return []

@app.command()
def compute_dynamic_weights(
    sport: str,
    market: str,
    strategy: str = "dynamic_hybrid",
    config_dir: str = "configs/dynamic_weighting"
):
    typer.echo(f"Computing dynamic weights for {sport} - {market} using {strategy}")

    # Load configs
    try:
        policy_data = _load_yaml(f"{config_dir}/default.yaml")
        family_priors = _load_yaml(f"{config_dir}/family_priors.yaml")
    except FileNotFoundError:
        typer.echo(f"Warning: Configs not found in {config_dir}, using defaults.", err=True)
        policy_data = {
            "name": "default_policy", "description": "Fallback policy",
            "min_weight_floor": 0.05, "max_weight_cap": 0.8,
            "trust_component_weight": 1.0, "regime_component_weight": 1.0,
            "disagreement_penalty_weight": 1.0, "recency_penalty_weight": 1.0,
            "calibrated_bonus": 0.1
        }
        family_priors = {"default": {}}

    config = {"family_priors": family_priors}
    policy_data["name"] = f"{sport}_{market}_policy"
    policy_data["description"] = f"Auto-generated policy for {sport} {market}"

    runner = DynamicWeightingRunner(strategy, policy_data, config)

    # Mock data
    sources = _get_mock_eligible_sources(sport, market)
    context = {"event_id": f"evt_{sport}_{market}_1", "sport": sport, "market_type": market}

    weights, diagnostics = runner.run(sources, context)

    typer.echo(f"\nEligible source count: {diagnostics.source_count}")
    typer.echo(f"Selected weighting strategy: {strategy}")

    typer.echo("\nFinal Normalized Weights:")
    for w in sorted(weights, key=lambda x: x.final_weight, reverse=True):
        typer.echo(f"  - {w.source_name} ({w.source_family}): {w.final_weight:.4f}")
        typer.echo(f"    Explanation: {w.explanation_summary}")

    typer.echo("\nDiagnostics:")
    if diagnostics.capped_sources:
        typer.echo(f"  - Capped sources: {', '.join(diagnostics.capped_sources)}")
    if diagnostics.floored_sources:
        typer.echo(f"  - Floored sources: {', '.join(diagnostics.floored_sources)}")
    if diagnostics.stale_penalties:
        typer.echo(f"  - Stale penalties applied: {', '.join(diagnostics.stale_penalties)}")

    # Create dummy manifest
    manifest = WeightingManifest(
        run_id="test_run_1",
        sport=sport,
        market_type=market,
        event_count=1,
        decisions=[WeightingDecisionRecord(event_id=context["event_id"], sport=sport, market_type=market, policy=policy_data["name"], decisions=weights)],
        diagnostics=[diagnostics]
    )

    path = save_weighting_manifest(manifest, "results/weighting")
    typer.echo(f"\nArtifact saved to: {path}")

@app.command()
def preview_weight_breakdown(sport: str, market: str):
    # Alias for compute for now to show breakdown
    compute_dynamic_weights(sport, market)

@app.command()
def preview_weight_diagnostics(sport: str, market: str):
    compute_dynamic_weights(sport, market)

@app.command()
def list_weighting_strategies():
    strategies = weighting_registry.list_strategies()
    typer.echo("Available Weighting Strategies:")
    for s in strategies:
        typer.echo(f"  - {s}")

if __name__ == "__main__":
    app()

@app.command()
def run_ensemble(
    sport: str,
    market: str,
    weighting: str = typer.Option("dynamic_hybrid", "--weighting", "-w")
):
    typer.echo(f"Running ensemble for {sport} - {market} with weighting: {weighting}")

    runner = DynamicWeightingRunner(weighting, {
            "name": f"policy_{weighting}", "description": "",
            "min_weight_floor": 0.05, "max_weight_cap": 0.8,
            "trust_component_weight": 1.0, "regime_component_weight": 1.0,
            "disagreement_penalty_weight": 1.0, "recency_penalty_weight": 1.0,
            "calibrated_bonus": 0.1
        }, {"family_priors": {"default": {}}})

    sources = _get_mock_eligible_sources(sport, market)
    context = {"event_id": f"evt_{sport}_{market}_2", "sport": sport, "market_type": market}

    weights, diagnostics = runner.run(sources, context)

    # Map back to EnsembleInputRecord
    from sports_signal_bot.ensemble.contracts import EnsembleInputRecord, StandardizedPredictionRecord

    preds = []
    for i, s in enumerate(sources):
        w_record = next((w for w in weights if w.source_name == s['name']), None)

        preds.append(StandardizedPredictionRecord(
            event_id=context["event_id"],
            sport=sport,
            market_type=market,
            source_name=s['name'],
            source_family=s['family'],
            class_labels=["A", "B"],
            probabilities={"A": s['probability'], "B": 1.0 - s['probability']},
            predicted_class="A" if s['probability'] > 0.5 else "B",
            metadata={"dynamic_weight": w_record.final_weight, "dynamic_weight_explanation": w_record.explanation_summary} if w_record else {}
        ))

    input_rec = EnsembleInputRecord(
        event_id=context["event_id"],
        sport=sport,
        market_type=market,
        predictions=preds
    )

    from sports_signal_bot.ensemble.runner import EnsembleRunner
    config = {
        "strategy": "dynamic_weighted_average",
        "strategy_config": {}
    }

    ens_runner = EnsembleRunner(config)
    res = ens_runner.run([input_rec])

    out = res["outputs"][0]

    typer.echo("\nEnsemble Results:")
    typer.echo(f"  Final Probabilities: {out.final_probabilities}")
    typer.echo(f"  Predicted Class: {out.final_predicted_class}")
    typer.echo("\nComponent Sources (with weights):")
    for comp in out.component_sources:
        typer.echo(f"  - {comp.source_name}: {comp.weight:.4f}")
        typer.echo(f"    {comp.status}")
