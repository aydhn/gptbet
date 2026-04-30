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
    else:
        typer.echo("All documents are fresh.")

@docs_app.command("preview-coverage")
def preview_coverage():
    """Check documentation coverage for critical components."""
    registry = DocRegistry("docs")
    registry.scan()
    checker = DocCoverageChecker(registry)
    results = checker.check_coverage()
    typer.echo("Coverage Report generated.")

from sports_signal_bot.deployment.cli import app as deploy_app
app.add_typer(deploy_app, name='deploy')

reconcile_app = typer.Typer(help="Reconciliation and arbitration commands")
app.add_typer(reconcile_app, name="reconciliation")

@reconcile_app.command("run")
def run_reconciliation_cmd(sport: str, family: str, mode: str = "balanced_consensus"):
    typer.echo(f"Running reconciliation for sport={sport}, family={family}, mode={mode}")

from sports_signal_bot.evidence.cli import app as evidence_app
app.add_typer(evidence_app, name="evidence")

if __name__ == "__main__":
    app()
