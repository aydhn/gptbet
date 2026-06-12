import json
from datetime import datetime

import typer

from .cases import AdjudicationCaseBuilder
from .contracts import (
    AdjudicationCaseFamily,
    AdjudicationCaseStatus,
    AdjudicationSeverity,
    ResolutionInput,
    ResolutionType,
)
from .queue import AdjudicationQueueBuilder, AdjudicationRegistry
from .resolutions import ResolutionApplier

app = typer.Typer(help="Adjudication and Knowledge Memory commands")

registry = AdjudicationRegistry()
queue_builder = AdjudicationQueueBuilder(registry)


@app.command("run-adjudication")
def run_adjudication(case_id: str):
    """Run adjudication evaluation for a specific case."""
    case = registry.get_case(case_id)
    if not case:
        typer.echo(f"Case {case_id} not found.")
        return
    typer.echo(f"Running adjudication for case: {case.case_id}")
    typer.echo(f"Type: {case.case_type.value}, Severity: {case.severity.value}")


@app.command("list-adjudication-cases")
def list_adjudication_cases():
    """List all adjudication cases."""
    cases = registry.list_cases()
    if not cases:
        typer.echo("No cases found.")
        return
    for c in cases:
        typer.echo(
            f"- {c.case_id} ({c.case_type.value}) - Status: {c.current_status.value}"
        )


@app.command("preview-adjudication-queue")
def preview_adjudication_queue():
    """Preview the current adjudication queue."""
    queue = queue_builder.build_queue()
    typer.echo(f"Queue ID: {queue.queue_id}")
    typer.echo(f"Total queued cases: {len(queue.cases)}")
    for c in queue.cases:
        typer.echo(f"  [{c.queue_priority.value}] {c.case_id} ({c.case_type.value})")


@app.command("resolve-adjudication-case")
def resolve_adjudication_case(case_id: str, operator_id: str):
    """Resolve an adjudication case."""
    # Dummy resolution for CLI
    typer.echo(f"Operator {operator_id} resolving case {case_id}...")
    resolution = ResolutionApplier.create_resolution(
        ResolutionInput(
            case_id=case_id,
            resolution_type=ResolutionType.accept_source_a_over_b,
            feedback_eligibility=True,
            memory_write_allowed=True,
            effective_scope="single_entity",
        )
    )
    typer.echo(f"Resolution applied. Artifact ID: {resolution.resolution_id}")
    typer.echo(
        f"Feedback Status: {'Eligible' if resolution.feedback_eligibility else 'Ineligible'}"
    )


@app.command("preview-precedents")
def preview_precedents(case_id: str):
    """Preview matching precedents for a case."""
    typer.echo(f"Looking up precedents for case {case_id}...")
    typer.echo("No active precedents found (skeleton mode).")


@app.command("preview-knowledge-memory")
def preview_knowledge_memory():
    """Preview current knowledge memory entries."""
    typer.echo("Knowledge Memory is currently empty.")


@app.command("list-adjudication-strategies")
def list_adjudication_strategies():
    """List available adjudication strategies."""
    strats = [
        "ConservativeAdjudicationStrategy",
        "BalancedKnowledgeCaptureStrategy",
        "ReviewHeavyStrategy",
        "AliasFocusedResolutionStrategy",
        "ProviderReliabilityStrategy",
    ]
    for s in strats:
        typer.echo(f"- {s}")
