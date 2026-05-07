import typer
import json
import uuid
from typing import Optional
from src.sports_signal_bot.final_convergence_hardening import (
    build_final_hardening_convergence,
    build_frozen_baseline,
    build_production_readiness_review_surface,
    build_terminal_acceptance_pack,
    ConvergenceInputRecord,
    BaselineInputRecord,
    BaselineScopeRecord,
    ReviewSurfaceSectionRecord,
    AcceptancePackSectionRecord,
    ConvergenceBlockerRecord,
    build_final_convergence_matrix,
    summarize_final_convergence_matrix,
    build_final_convergence_budgets,
    summarize_final_convergence_budgets,
    measure_final_convergence_budget_consumption,
    ConvergenceFreshnessRecord
)
from src.sports_signal_bot.final_convergence_hardening.strategies import (
    ConservativeFinalConvergenceStrategy,
    BalancedConvergenceReadinessStrategy,
    BaselineTruthFirstStrategy,
    AcceptanceHonestyFirstStrategy
)

app = typer.Typer(help="Final Convergence Hardening CLI (Post-100 Pack 20)")

@app.command("run-hardening-pack-20")
def run_hardening_pack_20(strategy: str = "conservative"):
    typer.echo("Running Final Convergence Hardening Pack 20...")

    # 1. Convergence
    inputs = [ConvergenceInputRecord(input_id="inp_1", source_layer="validation", is_stale=False)]
    convergence = build_final_hardening_convergence("final_readiness_convergence", inputs)

    # 2. Baseline
    b_inputs = [BaselineInputRecord(input_id="binp_1", description="Valid proof")]
    b_scopes = [BaselineScopeRecord(scope_id="scp_1", scope_type="scheduler_truth_scope")]
    baseline = build_frozen_baseline("release_gating_baseline", b_inputs, b_scopes)

    # 3. Review Surface
    r_sections = [ReviewSurfaceSectionRecord(section_id="sec_1", section_type="production_readiness_section")]
    review = build_production_readiness_review_surface("release_readiness_review_surface", r_sections)

    # 4. Acceptance Pack
    a_sections = [AcceptancePackSectionRecord(section_id="asec_1", section_type="baseline_section")]
    acceptance = build_terminal_acceptance_pack("final_readiness_acceptance_pack", a_sections)

    # Integration
    matrix = build_final_convergence_matrix(convergence, baseline, review, acceptance)

    # Apply strategy
    strat_map = {
        "conservative": ConservativeFinalConvergenceStrategy(),
        "balanced": BalancedConvergenceReadinessStrategy(),
        "baseline_truth": BaselineTruthFirstStrategy(),
        "acceptance_honesty": AcceptanceHonestyFirstStrategy()
    }

    active_strat = strat_map.get(strategy, ConservativeFinalConvergenceStrategy())
    data = {
        "convergence": convergence,
        "baseline": baseline,
        "review": review,
        "acceptance": acceptance,
        "matrix": matrix
    }

    is_valid = active_strat.evaluate(data)

    typer.echo(f"Strategy '{strategy}' evaluation result: {'Passed' if is_valid else 'Failed'}")

    # Save artifacts
    with open("final_hardening_convergence.json", "w") as f:
        f.write(convergence.model_dump_json(indent=2))

    with open("frozen_baselines.json", "w") as f:
        f.write(baseline.model_dump_json(indent=2))

    with open("production_readiness_review_surfaces.json", "w") as f:
        f.write(review.model_dump_json(indent=2))

    with open("terminal_acceptance_packs.json", "w") as f:
        f.write(acceptance.model_dump_json(indent=2))

    with open("final_convergence_matrix.json", "w") as f:
        json.dump(matrix, f, indent=2)

    typer.echo("Artifacts generated:")
    typer.echo("- final_hardening_convergence.json")
    typer.echo("- frozen_baselines.json")
    typer.echo("- production_readiness_review_surfaces.json")
    typer.echo("- terminal_acceptance_packs.json")
    typer.echo("- final_convergence_matrix.json")


@app.command("preview-final-convergence-report")
def preview_final_convergence_report():
    try:
        with open("final_hardening_convergence.json", "r") as f:
            data = json.load(f)
            typer.echo(f"Convergence Family: {data['convergence_family']}")
            typer.echo(f"Status: {data['convergence_status']}")
            typer.echo(f"Input Count: {len(data['input_refs'])}")
            typer.echo(f"Blocker Count: {len(data['blocker_refs'])}")
            typer.echo(f"Residue Count: {len(data['residue_refs'])}")
            if data['warnings']:
                typer.echo("Warnings:")
                for w in data['warnings']:
                    typer.echo(f" - {w}")
    except FileNotFoundError:
        typer.echo("Report not found. Run 'run-hardening-pack-20' first.")

@app.command("preview-frozen-baseline-report")
def preview_frozen_baseline_report():
     try:
         with open("frozen_baselines.json", "r") as f:
             data = json.load(f)
             typer.echo(f"Baseline Family: {data['baseline_family']}")
             typer.echo(f"Status: {data['baseline_status']}")
             typer.echo(f"Scope Count: {len(data['scope_refs'])}")
             typer.echo(f"Input Count: {len(data['input_refs'])}")
             typer.echo(f"Drift Count: {len(data['drift_refs'])}")
     except FileNotFoundError:
         typer.echo("Report not found. Run 'run-hardening-pack-20' first.")

@app.command("preview-readiness-review-report")
def preview_readiness_review_report():
     try:
         with open("production_readiness_review_surfaces.json", "r") as f:
             data = json.load(f)
             typer.echo(f"Surface Family: {data['surface_family']}")
             typer.echo(f"Status: {data['surface_status']}")
             typer.echo(f"Section Count: {len(data['section_refs'])}")
             typer.echo(f"Blocker Count: {len(data['blocker_refs'])}")
     except FileNotFoundError:
         typer.echo("Report not found. Run 'run-hardening-pack-20' first.")

@app.command("preview-terminal-acceptance-report")
def preview_terminal_acceptance_report():
     try:
         with open("terminal_acceptance_packs.json", "r") as f:
             data = json.load(f)
             typer.echo(f"Pack Family: {data['pack_family']}")
             typer.echo(f"Status: {data['pack_status']}")
             typer.echo(f"Section Count: {len(data['section_refs'])}")
             typer.echo(f"Evidence Count: {len(data['evidence_refs'])}")
             typer.echo(f"Replay Count: {len(data['replay_refs'])}")
     except FileNotFoundError:
         typer.echo("Report not found. Run 'run-hardening-pack-20' first.")

@app.command("preview-final-convergence-health")
def preview_final_convergence_health():
    try:
        with open("final_convergence_matrix.json", "r") as f:
            matrix = json.load(f)
            summary = summarize_final_convergence_matrix(matrix)
            typer.echo(f"Surfaces Evaluated: {summary['surfaces_evaluated']}")
            typer.echo(f"All Verified: {summary['all_verified']}")
            typer.echo(f"All Blockers Explicit: {summary['all_blockers_explicit']}")

            # Budgets
            budgets = build_final_convergence_budgets()
            consumptions = measure_final_convergence_budget_consumption(budgets)
            b_summary = summarize_final_convergence_budgets(budgets, consumptions)
            typer.echo(f"Total Budgets: {b_summary['total_budgets']}")
            typer.echo(f"Consumptions: {b_summary['consumptions']}")

    except FileNotFoundError:
        typer.echo("Matrix/Reports not found. Run 'run-hardening-pack-20' first.")

@app.command("list-final-convergence-strategies")
def list_final_convergence_strategies():
    typer.echo("Available Strategies:")
    typer.echo("1. conservative (ConservativeFinalConvergenceStrategy)")
    typer.echo("2. balanced (BalancedConvergenceReadinessStrategy)")
    typer.echo("3. baseline_truth (BaselineTruthFirstStrategy)")
    typer.echo("4. acceptance_honesty (AcceptanceHonestyFirstStrategy)")
