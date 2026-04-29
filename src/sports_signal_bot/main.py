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

if __name__ == "__main__":
    app()
