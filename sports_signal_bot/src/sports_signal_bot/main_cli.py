import os
import uuid

import typer
import yaml

# Dummy imports to simulate classifiers registration
from sports_signal_bot.regimes import (RegimeConfig, RegimeFactory,
                                       RegimeRegistry, RegimeRunner,
                                       RegimeThresholdsConfig,
                                       build_event_regime_inputs,
                                       build_period_regime_inputs,
                                       build_regime_manifest,
                                       calculate_coverage,
                                       export_event_regimes_csv,
                                       export_period_regimes_csv,
                                       export_regime_manifest,
                                       generate_regime_summary)

# Assuming app is already defined in main.py, we will just patch it
app = typer.Typer(help="Sports Signal Bot CLI")


def _load_configs(sport: str):
    with open("configs/regimes/thresholds.yaml") as f:
        t_data = yaml.safe_load(f)
    t_config = RegimeThresholdsConfig(**t_data)

    with open(f"configs/regimes/{sport}.yaml") as f:
        r_data = yaml.safe_load(f)
    r_config = RegimeConfig(**r_data)

    return t_config, r_config


@app.command()
def list_regime_families():
    """Lists active regime families"""
    event_families = list(RegimeRegistry.get_event_classifiers().keys())
    period_families = list(RegimeRegistry.get_period_classifiers().keys())

    typer.echo("Active Event Regime Families:")
    for f in event_families:
        typer.echo(f"  - {f}")

    typer.echo("Active Period Regime Families:")
    for f in period_families:
        typer.echo(f"  - {f}")


@app.command()
def assign_regimes(sport: str = typer.Option(...), market: str = typer.Option(...)):
    """Assign regimes to events"""
    t_config, r_config = _load_configs(sport)
    factory = RegimeFactory(t_config, r_config)
    runner = RegimeRunner(factory)

    # Mock data
    inputs = build_event_regime_inputs(
        event_id="evt_123",
        sport=sport,
        market_type=market,
        features={
            "home_form_score": 0.8,
            "away_form_score": 0.2,
            "home_rest_days": 2,
            "away_rest_days": 4,
        },
        ensemble_probabilities={"home": 0.7, "away": 0.3},
        source_probabilities={
            "bookie1": {"home": 0.75, "away": 0.25},
            "bookie2": {"home": 0.65, "away": 0.35},
        },
    )

    result = runner.assign_event_regimes(inputs)

    typer.echo(
        f"Assigned {len(result.event_regimes)} event regimes for {sport} {market}"
    )
    for r in result.event_regimes:
        typer.echo(
            f"  - {r.regime_family}: {r.regime_label} (method: {r.assignment_method})"
        )

    os.makedirs("results/regimes", exist_ok=True)
    export_event_regimes_csv(result.event_regimes, "results/regimes/event_regimes.csv")
    typer.echo("Saved to results/regimes/event_regimes.csv")


@app.command()
def preview_regime_coverage(
    sport: str = typer.Option(...), market: str = typer.Option(...)
):
    """Preview regime coverage"""
    t_config, r_config = _load_configs(sport)
    factory = RegimeFactory(t_config, r_config)
    runner = RegimeRunner(factory)

    # Mock multiple events
    records = []
    for i in range(150):  # Above min threshold
        inputs = build_event_regime_inputs(
            event_id=f"evt_{i}",
            sport=sport,
            market_type=market,
            features={"home_form_score": 0.8, "away_form_score": 0.2},
            ensemble_probabilities={"home": 0.7, "away": 0.3},
        )
        res = runner.assign_event_regimes(inputs)
        records.extend(res.event_regimes)

    coverages = calculate_coverage(records, t_config)
    manifest = build_regime_manifest(
        run_id=str(uuid.uuid4()),
        active_families=r_config.enabled_regime_families,
        coverages=coverages,
        evaluations=[],
    )

    typer.echo(generate_regime_summary(manifest))

    os.makedirs("results/regimes", exist_ok=True)
    export_regime_manifest(manifest, "results/regimes/regime_manifest.json")
    typer.echo("Saved manifest to results/regimes/regime_manifest.json")


@app.command()
def preview_regime_leaderboard(
    sport: str = typer.Option(...), market: str = typer.Option(...)
):
    """Preview leaderboard by regime"""
    typer.echo(f"Previewing regime leaderboard for {sport} {market}")
    typer.echo("Note: Real evaluation integration is mocked in this command.")
    typer.echo("  - Regime: market_disagreement: high_source_disagreement")
    typer.echo("    1. Source A (LogLoss: 0.65)")
    typer.echo("    2. Source B (LogLoss: 0.68)")


@app.command()
def preview_period_regimes(
    sport: str = typer.Option(...), market: str = typer.Option(...)
):
    """Preview period regimes"""
    t_config, r_config = _load_configs(sport)
    factory = RegimeFactory(t_config, r_config)
    runner = RegimeRunner(factory)

    inputs = build_period_regime_inputs(
        period_id=1,
        sport=sport,
        market_type=market,
        historical_metrics=[{"log_loss": 0.6}, {"log_loss": 0.65}],
    )
    result = runner.assign_period_regimes(inputs)

    typer.echo(f"Assigned period regimes for {sport} {market}")
    for r in result.period_regimes:
        typer.echo(f"  - {r.regime_family}: {r.regime_label}")

    os.makedirs("results/regimes", exist_ok=True)
    export_period_regimes_csv(
        result.period_regimes, "results/regimes/period_regimes.csv"
    )
    typer.echo("Saved to results/regimes/period_regimes.csv")


if __name__ == "__main__":
    app()

# --- SOURCE SELECTION COMMANDS ---

from pathlib import Path

from rich.console import Console

from sports_signal_bot.source_selection.catalog import (SourceCatalog,
                                                        SourceCatalogEntry)
from sports_signal_bot.source_selection.chain import SourcePolicyChain
from sports_signal_bot.source_selection.contracts import SourcePolicyDefinition
from sports_signal_bot.source_selection.metadata import SourceMetadataLoader
from sports_signal_bot.source_selection.runner import SourceSelectionRunner
from sports_signal_bot.source_selection.scoring import SourceTrustScorer


def _build_source_runner(sport: str) -> SourceSelectionRunner:
    # 1. Load config
    try:
        with open(f"configs/source_selection/{sport}.yaml") as f:
            sport_config = yaml.safe_load(f)
    except FileNotFoundError:
        sport_config = {}

    try:
        with open("configs/source_selection/trust_weights.yaml") as f:
            weights = yaml.safe_load(f)
    except FileNotFoundError:
        weights = None

    try:
        with open("configs/source_selection/policies.yaml") as f:
            policies_data = yaml.safe_load(f)
            policy_defs = [
                SourcePolicyDefinition(**p) for p in policies_data.get("policies", [])
            ]
    except FileNotFoundError:
        policy_defs = [
            SourcePolicyDefinition(policy_name="BasicAvailabilityPolicy"),
            SourcePolicyDefinition(policy_name="FallbackSafetyPolicy"),
        ]

    # Override fallback from sport config if present
    for p in policy_defs:
        if (
            p.policy_name == "FallbackSafetyPolicy"
            and "fallback_source_priority" in sport_config
        ):
            p.parameters["fallback_source_priority"] = sport_config[
                "fallback_source_priority"
            ]

    # 2. Build mock catalog for demonstration
    entries = [
        SourceCatalogEntry(
            source_name="football_poisson_core",
            source_family="poisson",
            supported_sports=["football"],
            supported_markets=["1x2", "ou_2_5"],
        ),
        SourceCatalogEntry(
            source_name="elo_rating_source",
            source_family="rating",
            supported_sports=["football", "basketball"],
            supported_markets=["1x2", "moneyline"],
        ),
        SourceCatalogEntry(
            source_name="calibrated_logistic",
            source_family="ml",
            supported_sports=["football", "basketball"],
            supported_markets=["1x2", "moneyline", "ou_2_5"],
            requires_calibration=True,
        ),
        SourceCatalogEntry(
            source_name="raw_logistic",
            source_family="ml",
            supported_sports=["football", "basketball"],
            supported_markets=["1x2", "moneyline", "ou_2_5"],
        ),
        SourceCatalogEntry(
            source_name="basketball_structural_core",
            source_family="structural",
            supported_sports=["basketball"],
            supported_markets=["moneyline"],
        ),
        SourceCatalogEntry(
            source_name="bookmaker_implied",
            source_family="market",
            supported_sports=["football"],
            supported_markets=["ou_2_5"],
        ),
    ]
    catalog = SourceCatalog(entries)

    # 3. Assemble runner
    return SourceSelectionRunner(
        catalog=catalog,
        metadata_loader=SourceMetadataLoader(),
        scorer=SourceTrustScorer(weights=weights),
        policy_chain=SourcePolicyChain(policy_definitions=policy_defs),
        manifest_dir=Path("results/manifests/selection"),
        report_dir=Path("results/reports/selection"),
    )


@app.command()
def select_sources(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    event_id: str = typer.Option("mock_event_123", help="Event ID"),
):
    """Run full source selection and generate manifest."""
    console = Console()
    console.print(
        f"[bold blue]Running source selection for {sport} - {market}...[/bold blue]"
    )

    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print("[green]Selection complete![/green]")
    console.print(f"Candidates evaluated: {manifest.summary.total_candidates}")
    console.print(f"Eligible sources: {manifest.summary.eligible_count}")
    console.print(f"Selected: {', '.join(manifest.selected_sources)}")
    console.print(f"Fallback used: {manifest.summary.fallback_used}")
    console.print(f"Manifest written to results/manifests/selection/{manifest.run_id}")


@app.command()
def preview_source_trust(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    event_id: str = typer.Option("mock_event_123", help="Event ID"),
):
    """Preview trust scores for candidate sources."""
    console = Console()
    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print(f"\n[bold]Trust Scores Preview ({sport} - {market})[/bold]")
    for d in manifest.decisions:
        if d.eligibility_record.trust_score:
            console.print(
                f"- {d.source_name}: {d.eligibility_record.trust_score.total_trust_score:.3f}"
            )


@app.command()
def preview_source_exclusions(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    event_id: str = typer.Option("mock_event_123", help="Event ID"),
):
    """Preview exclusion reasons for an event."""
    console = Console()
    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print(f"\n[bold]Exclusions Preview ({sport} - {market})[/bold]")
    if manifest.summary.excluded_count == 0:
        console.print("No sources were excluded.")
    else:
        for d in manifest.decisions:
            if not d.is_selected:
                reasons = ", ".join(
                    [ex.reason_code for ex in d.eligibility_record.exclusion_reasons]
                )
                console.print(f"- {d.source_name} excluded: {reasons}")


@app.command()
def preview_source_eligibility(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    event_id: str = typer.Option("mock_event_123", help="Event ID"),
):
    """Preview final eligibility status of sources."""
    console = Console()
    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print(f"\n[bold]Eligibility Preview ({sport} - {market})[/bold]")
    for d in manifest.decisions:
        status = "[green]ELIGIBLE[/green]" if d.is_selected else "[red]EXCLUDED[/red]"
        console.print(f"{status} - {d.source_name}")


@app.command()
def list_source_policies():
    """List currently configured eligibility policies."""
    console = Console()
    try:
        with open("configs/source_selection/policies.yaml") as f:
            policies_data = yaml.safe_load(f)

        console.print("\n[bold]Configured Source Policies:[/bold]")
        for p in policies_data.get("policies", []):
            status = (
                "[green]Enabled[/green]"
                if p.get("is_enabled", True)
                else "[red]Disabled[/red]"
            )
            console.print(f"- {p['policy_name']} ({status})")
            if p.get("parameters"):
                for k, v in p["parameters"].items():
                    console.print(f"    {k}: {v}")
    except FileNotFoundError:
        console.print("[red]Policy configuration file not found.[/red]")


from rich.console import Console

console = Console()

from sports_signal_bot.core.paths import get_configs_dir


def register_signal_scoring_commands(app: typer.Typer):

    @app.command(name="score-signals")
    def score_signals(
        sport: str = typer.Option(
            ..., "--sport", "-s", help="Sport name (e.g. football, basketball)"
        ),
        market: str = typer.Option(
            ..., "--market", "-m", help="Market type (e.g. 1x2, moneyline)"
        ),
        strategy: str = typer.Option(
            None, "--strategy", help="Specific scoring strategy to use"
        ),
        config: str = typer.Option(
            None, "--config", "-c", help="Path to specific signal scoring config file"
        ),
    ):
        """Scores final probabilities into operational signals (Phase 17)."""
        from sports_signal_bot.signal_scoring.contracts import \
            SignalCandidateRecord
        from sports_signal_bot.signal_scoring.runner import SignalScoringRunner

        console.print(f"[bold cyan]Scoring Signals for {sport} - {market}[/bold cyan]")

        config_dir = get_configs_dir()
        default_config_path = config_dir / "signal_scoring" / "default.yaml"
        sport_config_path = config_dir / "signal_scoring" / f"{sport}.yaml"

        scoring_config = {}

        if default_config_path.exists():
            with open(default_config_path, "r") as f:
                scoring_config.update(yaml.safe_load(f) or {})

        if sport_config_path.exists():
            with open(sport_config_path, "r") as f:
                sport_specific = yaml.safe_load(f) or {}
                for k, v in sport_specific.items():
                    if (
                        isinstance(v, dict)
                        and k in scoring_config
                        and isinstance(scoring_config[k], dict)
                    ):
                        scoring_config[k].update(v)
                    else:
                        scoring_config[k] = v

        candidates = [
            SignalCandidateRecord(
                event_id=f"event_{i}",
                sport=sport,
                market_type=market,
                selection="home" if i % 2 == 0 else "away",
                final_probability=0.55 + (i * 0.02),
                market_implied_probability=0.50 + (i * 0.01) if i % 3 != 0 else None,
                class_probabilities={"home": 0.55, "draw": 0.25, "away": 0.20},
                metadata={
                    "source_disagreement_diagnostics": {
                        "source_variance": 0.02 + (i * 0.01)
                    },
                    "data_quality_summaries": {"missing_feature_ratio": 0.05},
                    "source_selection_diagnostics": {"stale_components_ratio": 0.0},
                    "regime_assignments": [
                        {"regime_family": "data_completeness", "regime_label": "high"}
                    ],
                },
            )
            for i in range(10)
        ]

        results_dir = Path("results/signal_scoring")
        runner = SignalScoringRunner(scoring_config, str(results_dir))

        manifest = runner.run(candidates, sport, market, strategy_name=strategy)

        console.print(
            f"[green]Scoring Complete.[/green] Total processed: {manifest.total_processed}"
        )
        console.print(
            f"Scored: {manifest.scored_count}, Weak: {manifest.weak_signal_count}, No Ref: {manifest.no_market_reference_count}"
        )
        if manifest.top_signals:
            console.print(
                f"Top signal: {manifest.top_signals[0].event_id} ({manifest.top_signals[0].tier} tier)"
            )
        console.print(
            f"Artifacts saved in: {results_dir}/{sport}/{market}/{manifest.run_id}"
        )

    @app.command(name="preview-signal-breakdown")
    def preview_signal_breakdown(
        sport: str = typer.Option(..., "--sport", "-s"),
        market: str = typer.Option(..., "--market", "-m"),
    ):
        """Previews signal score components breakdown (Phase 17)."""
        console.print(
            f"[bold yellow]Signal Breakdown Preview: {sport} - {market}[/bold yellow]"
        )
        console.print(
            "This command reads the latest signal scores and displays component breakdown."
        )

    @app.command(name="preview-signal-ranking")
    def preview_signal_ranking(
        sport: str = typer.Option(..., "--sport", "-s"),
        market: str = typer.Option(..., "--market", "-m"),
    ):
        """Previews top ranked signals (Phase 17)."""
        console.print(
            f"[bold magenta]Signal Ranking Preview: {sport} - {market}[/bold magenta]"
        )
        console.print(
            "This command displays the top tier signals based on the latest run."
        )

    @app.command(name="preview-signal-diagnostics")
    def preview_signal_diagnostics(
        sport: str = typer.Option(..., "--sport", "-s"),
        market: str = typer.Option(..., "--market", "-m"),
    ):
        """Previews signal quality diagnostics (Phase 17)."""
        console.print(
            f"[bold cyan]Signal Diagnostics Preview: {sport} - {market}[/bold cyan]"
        )
        console.print(
            "This command displays aggregate signal quality, coverage, and warnings."
        )

    @app.command(name="list-signal-strategies")
    def list_signal_strategies():
        """Lists available signal scoring strategies (Phase 17)."""
        from sports_signal_bot.signal_scoring.factory import \
            SignalScorerFactory  # Forces registration
        from sports_signal_bot.signal_scoring.registry import \
            SignalScorerRegistry

        strategies = SignalScorerRegistry.list_strategies()
        console.print("[bold green]Available Signal Scoring Strategies:[/bold green]")
        for name, cls in strategies.items():
            try:
                inst = cls({})
                desc = inst.describe()
            except Exception:
                desc = "No description available."
            console.print(f"  - [cyan]{name}[/cyan]: {desc}")


@app.command()
def list_threshold_strategies():
    """Lists available threshold optimization strategies"""
    from sports_signal_bot.thresholds.factory import ThresholdStrategyFactory
    from sports_signal_bot.thresholds.registry import ThresholdStrategyRegistry

    strategies = ThresholdStrategyRegistry.list_strategies()
    typer.echo(f"Available Threshold Strategies ({len(strategies)}):")
    for name, strategy_class in strategies.items():
        typer.echo(f"  - {name} ({strategy_class.__name__})")


@app.command()
def optimize_thresholds(
    sport: str = typer.Option(..., help="Sport (e.g., football, basketball)"),
    market: str = typer.Option(..., help="Market type (e.g., 1x2, moneyline)"),
    strategy: str = typer.Option("score_only", help="Optimization strategy"),
):
    """Run threshold optimization and generate frontier"""
    typer.echo(
        f"Running threshold optimization for {sport} - {market} using {strategy} strategy"
    )

    import os

    import pandas as pd
    import yaml

    from sports_signal_bot.signal_scoring.contracts import (
        SignalComponentRecord, SignalScoreRecord)
    from sports_signal_bot.thresholds.runner import ThresholdRunner

    config_path = f"configs/thresholds/{sport}.yaml"
    if not os.path.exists(config_path):
        config_path = "configs/thresholds/default.yaml"

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        config = {
            "sweep_engine": {
                "objective": {"objective_name": "precision_oriented"},
                "constraints": {"minimum_accepted_count": 1},
                "grid": {"score_threshold_bounds": [0.0, 1.0], "grid_steps": 10},
            }
        }

    # Mock data
    signals = [
        SignalScoreRecord(
            event_id=f"evt_{i}",
            sport=sport,
            market_type=market,
            selection="test",
            final_probability=0.6,
            components=SignalComponentRecord(
                edge_estimate=0.05, confidence_score=0.8, uncertainty_penalty=0.1
            ),
            final_signal_score=0.5 + (i * 0.05),
            strategy_name="test",
        )
        for i in range(10)
    ]

    labels_df = pd.DataFrame(
        [
            {"event_id": f"evt_{i}", "target_value": "test" if i % 2 == 0 else "other"}
            for i in range(10)
        ]
    )

    runner = ThresholdRunner(config)
    result = runner.optimize(strategy, signals, labels_df, sport, market)

    typer.echo(f"Evaluated {result.total_evaluated} threshold candidates.")

    if result.best_candidate:
        typer.echo(f"Best Candidate:")
        typer.echo(f"  Score Threshold: {result.best_candidate.score_threshold:.4f}")
        typer.echo(
            f"  Objective ({result.objective_name}): {result.best_candidate.objective_value:.4f}"
        )
        typer.echo(f"  Accepted Count: {result.best_candidate.accepted_count}")
        typer.echo(f"  Coverage Rate: {result.best_candidate.coverage_rate:.2%}")
        for k, v in result.best_candidate.quality_metrics.items():
            typer.echo(f"  {k}: {v:.4f}")
    else:
        typer.echo("No valid threshold found that satisfies constraints.")
        for w in result.warnings:
            typer.echo(f"  Warning: {w}")


@app.command()
def preview_threshold_frontier(
    sport: str = typer.Option(..., help="Sport (e.g., football, basketball)"),
    market: str = typer.Option(..., help="Market type (e.g., 1x2, moneyline)"),
):
    """Preview threshold tradeoff frontier"""
    typer.echo(f"Previewing threshold frontier for {sport} - {market}")
    typer.echo("Generating dummy candidates and building frontier...")

    from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord
    from sports_signal_bot.thresholds.frontier import ThresholdFrontierBuilder

    candidates = [
        ThresholdCandidateRecord(
            market_type=market,
            sport=sport,
            score_threshold=0.5 + (i * 0.05),
            accepted_count=100 - (i * 10),
            rejected_count=i * 10,
            coverage_rate=1.0 - (i * 0.1),
            acceptance_rate=1.0 - (i * 0.1),
            objective_value=0.5 + (i * 0.02),
            quality_metrics={"accuracy": 0.5 + (i * 0.02)},
        )
        for i in range(10)
    ]

    builder = ThresholdFrontierBuilder(candidates, sport, market)
    frontier = builder.build()
    summary = builder.summarize_tradeoff_curve(frontier)

    import json

    typer.echo(json.dumps(frontier.model_dump(), indent=2))
    typer.echo(f"Summary: {summary}")


@app.command()
def preview_accepted_signals(
    sport: str = typer.Option(..., help="Sport (e.g., football, basketball)"),
    market: str = typer.Option(..., help="Market type (e.g., 1x2, moneyline)"),
):
    """Preview accepted signals using a test policy"""
    typer.echo(f"Previewing accepted signals for {sport} - {market}")

    from sports_signal_bot.signal_scoring.contracts import (
        SignalComponentRecord, SignalScoreRecord)
    from sports_signal_bot.thresholds.contracts import ThresholdPolicyRecord
    from sports_signal_bot.thresholds.runner import ThresholdRunner

    runner = ThresholdRunner({})
    policy = ThresholdPolicyRecord(
        policy_name="test_policy",
        sport=sport,
        market_type=market,
        signal_strategy="score_only",
        threshold_type="min_signal_score",
        selected_threshold=0.7,
        optimization_objective="balanced",
    )

    signals = [
        SignalScoreRecord(
            event_id=f"evt_{i}",
            sport=sport,
            market_type=market,
            selection="test",
            final_probability=0.6,
            components=SignalComponentRecord(
                edge_estimate=0.05, confidence_score=0.8, uncertainty_penalty=0.1
            ),
            final_signal_score=0.5 + (i * 0.05),
            strategy_name="test",
        )
        for i in range(10)
    ]

    results = runner.apply_policy(policy, signals)

    accepted = [r for r in results if r.is_accepted]
    rejected = [r for r in results if not r.is_accepted]

    typer.echo(f"Total Signals: {len(results)}")
    typer.echo(f"Accepted Signals: {len(accepted)}")
    typer.echo(f"Rejected Signals: {len(rejected)}")


@app.command()
def preview_threshold_policy(
    sport: str = typer.Option(..., help="Sport (e.g., football, basketball)"),
    market: str = typer.Option(..., help="Market type (e.g., 1x2, moneyline)"),
):
    """Preview a generated threshold policy"""
    typer.echo(f"Previewing threshold policy for {sport} - {market}")

    from sports_signal_bot.thresholds.contracts import ThresholdPolicyRecord

    policy = ThresholdPolicyRecord(
        policy_name=f"{sport}_{market}_policy",
        sport=sport,
        market_type=market,
        signal_strategy="score_and_edge",
        threshold_type="min_score_and_edge",
        selected_threshold=0.65,
        edge_threshold=0.02,
        optimization_objective="balanced",
        training_reference_window="last_30_days",
        minimum_quality_constraints={"min_coverage": 0.1},
    )

    import json

    typer.echo(json.dumps(policy.model_dump(), indent=2, default=str))


# --- POLICY COMMANDS ---
from sports_signal_bot.policy.runner import PolicyRunner
from sports_signal_bot.signal_scoring.contracts import (
    SignalPolicyInputRecord, SignalStatus)


def _build_policy_runner(sport: str, strategy: str) -> PolicyRunner:
    import yaml

    try:
        with open(f"configs/policy/{sport}.yaml") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        try:
            with open("configs/policy/default.yaml") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {
                "score_bands": {"no_bet": 0.4, "watchlist": 0.6, "candidate": 0.8},
                "action_class_mapping": {
                    "approved": "approved_candidate",
                    "candidate": "candidate",
                    "watchlist": "watchlist",
                    "no_bet_zone": "no_action",
                    "blocked": "blocked_candidate",
                },
            }
    return PolicyRunner(config, strategy)


@app.command()
def apply_policy(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    policy: str = typer.Option(
        "balanced", help="Policy strategy (balanced/conservative/regime_aware)"
    ),
):
    """Run the policy engine to assign signal lifecycles and action classes."""
    typer.echo(f"Running policy engine for {sport} - {market} using {policy} strategy")

    runner = _build_policy_runner(sport, policy)

    # Mock data
    signals = [
        SignalPolicyInputRecord(
            event_id=f"evt_{i}",
            sport=sport,
            market_type=market,
            selection="test",
            final_probability=0.6,
            final_signal_score=0.3 + (i * 0.1),
            edge_estimate=0.02 + (i * 0.01),
            status=SignalStatus.SCORED,
            components_summary={
                "uncertainty_penalty": 0.05,
                "disagreement_penalty": 0.1,
                "data_quality_penalty": 0.0,
                "market_implied_probability": 0.58,
            },
        )
        for i in range(8)
    ]

    # Add a blocked signal
    signals.append(
        SignalPolicyInputRecord(
            event_id="evt_blocked",
            sport=sport,
            market_type=market,
            selection="test",
            final_probability=0.6,
            final_signal_score=0.9,
            edge_estimate=0.05,
            status=SignalStatus.SCORED,
            components_summary={
                "data_quality_penalty": 0.8,  # Low quality
                "market_implied_probability": 0.58,
            },
        )
    )

    manifest = runner.run(signals, sport, market)

    typer.echo(f"Total Signals Evaluated: {manifest.total_evaluated}")
    typer.echo(f"Approved: {manifest.approved_count}")
    typer.echo(f"Candidate: {manifest.candidate_count}")
    typer.echo(f"Watchlist: {manifest.watchlist_count}")
    typer.echo(f"No Action / No Bet Zone: {manifest.no_action_count}")
    typer.echo(f"Blocked: {manifest.blocked_count}")

    typer.echo("\nTop Rationale Codes:")
    for code, count in sorted(
        manifest.top_rationale_codes.items(), key=lambda x: x[1], reverse=True
    )[:3]:
        typer.echo(f"  - {code}: {count}")

    from sports_signal_bot.policy.manifests import export_policy_manifest

    export_policy_manifest(manifest, f"results/policy/{sport}/{market}")
    typer.echo(f"Saved artifacts to results/policy/{sport}/{market}")


@app.command()
def preview_policy_decisions(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    """Preview decision outputs from the default policy."""
    apply_policy(sport=sport, market=market, policy="balanced")


@app.command()
def preview_no_bet_zones(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    """Preview signals that fall into the no-bet zone."""
    typer.echo(f"Previewing no-bet zones for {sport} - {market}")
    runner = _build_policy_runner(sport, "balanced")

    signals = [
        SignalPolicyInputRecord(
            event_id=f"evt_{i}",
            sport=sport,
            market_type=market,
            selection="test",
            final_probability=0.5,
            final_signal_score=0.5,
            edge_estimate=0.02,
            status=SignalStatus.SCORED,
            components_summary={
                "uncertainty_penalty": 0.4,
                "market_implied_probability": 0.48,
            },
        )
        for i in range(3)
    ]
    manifest = runner.run(signals, sport, market)
    for d in manifest.decisions:
        if d.signal_status.value == "no_bet_zone":
            typer.echo(f"Event {d.event_id}: No Bet Zone. Reasons: {d.no_bet_reasons}")


@app.command()
def preview_policy_rationale(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    """Preview rationale codes for a mixed set of signals."""
    typer.echo("Previewing rationale codes...")
    apply_policy(sport=sport, market=market, policy="balanced")


@app.command()
def list_policy_strategies():
    """List available policy strategies."""
    from sports_signal_bot.policy.registry import PolicyStrategyRegistry

    strategies = PolicyStrategyRegistry._strategies.keys()
    typer.echo("Available Policy Strategies:")
    for s in strategies:
        typer.echo(f"  - {s}")
