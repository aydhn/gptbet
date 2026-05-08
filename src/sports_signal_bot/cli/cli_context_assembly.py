import typer
from rich.console import Console
from .context_assembly import (
    build_trace_freshness_pipeline,
    build_observatory_exchange_board_pipeline,
    build_context_assembly_pipeline,
    get_context_assembly_kpis,
    generate_context_assembly_health_report,
    write_context_assembly_artifacts
)

app = typer.Typer(help="Phase 95: Context Assembly Operations")
console = Console()

@app.command("run-context-assembly-pass")
def run_context_assembly_pass():
    console.print("[bold green]Running Context Assembly Pass...[/bold green]")
    build_trace_freshness_pipeline()
    build_observatory_exchange_board_pipeline()
    build_context_assembly_pipeline()
    write_context_assembly_artifacts()
    console.print("Context Assembly Pass Complete. Artifacts written.")

@app.command("preview-trace-federations")
def preview_trace_federations():
    pipeline = build_trace_freshness_pipeline()
    console.print(f"Trace Federation Status: {pipeline['status']}")

@app.command("preview-proof-freshness-councils")
def preview_proof_freshness_councils():
    pipeline = build_trace_freshness_pipeline()
    console.print(f"Proof Freshness Council initialized: {pipeline['council'].proof_freshness_council_id}")

@app.command("preview-observatory-exchange-boards")
def preview_observatory_exchange_boards():
    pipeline = build_observatory_exchange_board_pipeline()
    console.print(f"Observatory Exchange Board Status: {pipeline['status']}")

@app.command("preview-context-assemblers")
def preview_context_assemblers():
    pipeline = build_context_assembly_pipeline()
    console.print(f"Context Assembler initialized: {pipeline['assembler'].context_assembler_id}")

@app.command("preview-context-assembly-health")
def preview_context_assembly_health():
    report = generate_context_assembly_health_report()
    console.print("[bold cyan]Context Assembly Health Report[/bold cyan]")
    for k, v in report['summary'].items():
        console.print(f"  {k}: {v}")
    console.print("[bold cyan]KPIs[/bold cyan]")
    for k, v in report['kpis'].items():
        console.print(f"  {k}: {v}")

@app.command("list-context-assembly-strategies")
def list_context_assembly_strategies():
    strategies = [
        "ConservativeContextAssemblerStrategy",
        "BalancedTraceFreshnessBoardStrategy",
        "ProofFreshnessFirstStrategy",
        "ObservatoryBoardStrictStrategy",
        "SovereigntyDominantContextStrategy"
    ]
    console.print("[bold blue]Available Context Assembly Strategies:[/bold blue]")
    for s in strategies:
        console.print(f" - {s}")
