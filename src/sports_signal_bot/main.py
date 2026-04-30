import typer
from pathlib import Path
import json

from sports_signal_bot.docs_ops.registry import DocRegistry
from sports_signal_bot.docs_ops.freshness import FreshnessReporter
from sports_signal_bot.docs_ops.lint import DocLintRunner
from sports_signal_bot.docs_ops.coverage import DocCoverageChecker
from sports_signal_bot.docs_ops.manifests import ManifestGenerator
from sports_signal_bot.docs_ops.contracts import DocFamily

app = typer.Typer(help="Sports Signal Bot CLI")
docs_app = typer.Typer(help="Documentation Operations")
app.add_typer(docs_app, name="docs")

@docs_app.command("preview-index")
def preview_index():
    """Preview the documentation index and generate manifest."""
    registry = DocRegistry("docs")
    registry.scan()
    generator = ManifestGenerator(registry)
    manifest = generator.generate()
    typer.echo(manifest.model_dump_json(indent=2))

    # Save output artifacts
    Path("results").mkdir(exist_ok=True)
    with open("results/docs_ops_manifest.json", "w") as f:
        f.write(manifest.model_dump_json(indent=2))

@docs_app.command("lint")
def lint_docs():
    """Run lint checks on all documentation."""
    registry = DocRegistry("docs")
    registry.scan()
    linter = DocLintRunner(registry)
    results = linter.lint_all()

    failed = [r for r in results if not r.passed]
    if failed:
        typer.echo(f"Found {len(failed)} documents with lint issues:")
        for r in failed:
            typer.echo(f"  {r.path}: {r.issues}")
    else:
        typer.echo("All documents passed linting.")

    Path("results").mkdir(exist_ok=True)
    with open("results/docs_lint_report.json", "w") as f:
        json.dump([r.model_dump() for r in results], f, indent=2)

@docs_app.command("preview-freshness")
def preview_freshness():
    """Check documentation freshness."""
    registry = DocRegistry("docs")
    registry.scan()
    reporter = FreshnessReporter(registry)
    results = reporter.check_all()

    stale = [r for r in results if r.is_stale]
    if stale:
        typer.echo(f"Found {len(stale)} stale documents:")
        for r in stale:
            typer.echo(f"  {r.doc_id} (Role: {r.owner_role})")
    else:
        typer.echo("All documents are fresh.")

    Path("results").mkdir(exist_ok=True)
    with open("results/docs_freshness_summary.json", "w") as f:
        json.dump([r.model_dump() for r in results], f, indent=2)

@docs_app.command("preview-coverage")
def preview_coverage():
    """Check documentation coverage for critical components."""
    registry = DocRegistry("docs")
    registry.scan()
    checker = DocCoverageChecker(registry)
    results = checker.check_coverage()

    typer.echo("Coverage Report:")
    for r in results:
        typer.echo(f"  {r.component}: Score {r.coverage_score:.2f}")

    Path("results").mkdir(exist_ok=True)
    with open("results/docs_coverage_report.json", "w") as f:
        json.dump([r.model_dump() for r in results], f, indent=2)

@docs_app.command("list-playbooks")
def list_playbooks():
    """List all incident playbooks."""
    registry = DocRegistry("docs")
    registry.scan()
    playbooks = [d for d in registry.list_documents() if d.doc_family == DocFamily.INCIDENT_PLAYBOOK]
    for p in playbooks:
        typer.echo(f"- {p.title} ({p.path})")

@docs_app.command("list-runbooks")
def list_runbooks():
    """List all runbooks."""
    registry = DocRegistry("docs")
    registry.scan()
    runbooks = [d for d in registry.list_documents() if d.doc_family == DocFamily.RUNBOOK]
    for r in runbooks:
        typer.echo(f"- {r.title} ({r.path})")

@docs_app.command("list-glossary-terms")
def list_glossary_terms():
    """List glossary terms."""
    typer.echo("Glossary terms parsed: Not fully implemented in this phase.")

from sports_signal_bot.deployment.cli import app as deploy_app
app.add_typer(deploy_app, name='deploy')




import typer
reconcile_app = typer.Typer(help="Reconciliation and arbitration commands")
app.add_typer(reconcile_app, name="reconciliation")


@reconcile_app.command("run")
def run_reconciliation_cmd(sport: str, family: str, mode: str = "balanced_consensus"):
    typer.echo(f"Running reconciliation for sport={sport}, family={family}, mode={mode}")
    from sports_signal_bot.reconciliation.contracts import SourceObservationRecord
    from sports_signal_bot.reconciliation.grouping import build_reconciliation_groups
    from sports_signal_bot.reconciliation.arbitration import run_arbitration
    from datetime import datetime

    # In a real run, this would fetch from the provider layer.
    # We load basic test samples to demonstrate grouping.
    obs1 = SourceObservationRecord(
        source_observation_id="obs1", provider_name="provider_a", provider_kind="primary",
        data_family=family, sport=sport, entity_type="match", entity_key="match_123",
        payload={"kickoff_time": "2023-10-01T15:00:00Z", "home_team": "Arsenal", "status": "live"},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(),
        provider_quality_score=0.9, provider_health_status="healthy", lineage_ref="ref1"
    )
    obs2 = SourceObservationRecord(
        source_observation_id="obs2", provider_name="provider_b", provider_kind="secondary",
        data_family=family, sport=sport, entity_type="match", entity_key="match_123",
        payload={"kickoff_time": "2023-10-01T15:15:00Z", "home_team": "Arsenal FC", "status": "live"},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(),
        provider_quality_score=0.8, provider_health_status="healthy", lineage_ref="ref2"
    )

    groups = build_reconciliation_groups([obs1, obs2])
    typer.echo(f"Built {len(groups)} reconciliation groups.")

    for group in groups:
        unified, conflicts, dispute = run_arbitration(group, strategy_name=mode)
        typer.echo(f"Conflicts detected: {len(conflicts)}")
        if dispute:
            typer.echo(f"Dispute raised: {dispute.reasons}")
        else:
            typer.echo(f"Unified record generated with confidence {unified.confidence_score}")
            typer.echo(f"Trusted Payload: {unified.trusted_payload}")
@reconcile_app.command("preview-conflicts")
def preview_conflicts_cmd(family: str):
    typer.echo(f"Previewing conflicts for {family}...")

@reconcile_app.command("preview-disputes")
def preview_disputes_cmd(family: str):
    typer.echo(f"Previewing disputes for {family}...")

@reconcile_app.command("list-strategies")
def list_strategies_cmd():
    typer.echo("Available reconciliation strategies:")
    typer.echo("- conservative_truth")
    typer.echo("- balanced_consensus")
    typer.echo("- freshness_weighted_odds")
    typer.echo("- stable_source_bias")
    typer.echo("- review_heavy_conflict")

if __name__ == "__main__":
    app()
