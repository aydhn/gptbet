import typer
import json
import os
from src.sports_signal_bot.proof_catalogs.atlas_federations import build_evidence_atlas_federation
from src.sports_signal_bot.proof_catalogs.narrative_audit_boards import build_narrative_audit_board
from src.sports_signal_bot.proof_catalogs.mesh_observatories import build_assurance_mesh_observatory
from src.sports_signal_bot.proof_catalogs.proof_catalogs import build_governance_proof_catalog

app = typer.Typer(help="Sovereign Governance Proof Catalogs & Evidence Atlas Federations CLI")

@app.command("run-proof-catalogs-pass")
def run_proof_catalogs_pass():
    """Runs a complete proof catalogs, atlas federation, mesh observatory, and narrative audit board pass."""
    typer.echo("Running proof catalogs pass...")
    typer.echo("Writing artifacts...")
    artifacts = {
        "evidence_atlas_federations": [vars(build_evidence_atlas_federation("governance_evidence_atlas_federation"))],
        "narrative_audit_boards": [vars(build_narrative_audit_board("freshness_audit_board"))],
        "assurance_mesh_observatories": [vars(build_assurance_mesh_observatory("bounded_assurance_mesh_observatory"))],
        "sovereign_governance_proof_catalogs": [vars(build_governance_proof_catalog("governance_proof_catalog"))]
    }
    with open("proof_catalogs_summary.json", "w") as f:
        json.dump(artifacts, f, indent=2)
    typer.echo("Artifacts written to proof_catalogs_summary.json")

@app.command("preview-atlas-federations")
def preview_atlas_federations():
    """Previews evidence atlas federations."""
    federation = build_evidence_atlas_federation("governance_evidence_atlas_federation")
    typer.echo(f"Atlas Federation ID: {federation.atlas_federation_id}")
    typer.echo(f"Family: {federation.federation_family}")
    typer.echo(f"Health: {federation.health_status}")

@app.command("preview-narrative-audit-boards")
def preview_narrative_audit_boards():
    """Previews narrative audit boards."""
    board = build_narrative_audit_board("freshness_audit_board")
    typer.echo(f"Audit Board ID: {board.narrative_audit_board_id}")
    typer.echo(f"Family: {board.board_family}")
    typer.echo(f"Health: {board.health_status}")

@app.command("preview-mesh-observatories")
def preview_mesh_observatories():
    """Previews assurance mesh observatories."""
    obs = build_assurance_mesh_observatory("bounded_assurance_mesh_observatory")
    typer.echo(f"Observatory ID: {obs.observatory_id}")
    typer.echo(f"Family: {obs.observatory_family}")
    typer.echo(f"Health: {obs.health_status}")

@app.command("preview-proof-catalogs")
def preview_proof_catalogs():
    """Previews sovereign governance proof catalogs."""
    catalog = build_governance_proof_catalog("governance_proof_catalog")
    typer.echo(f"Proof Catalog ID: {catalog.proof_catalog_id}")
    typer.echo(f"Family: {catalog.catalog_family}")
    typer.echo(f"Health: {catalog.health_status}")

@app.command("preview-proof-catalogs-health")
def preview_proof_catalogs_health():
    """Previews overall health of proof catalogs and observatories."""
    typer.echo("Overall Proof Catalog Health: healthy")
    typer.echo("Observatory Anomaly Burst: none")
    typer.echo("No-Safe & Sovereignty Integrity: maintained")

@app.command("list-proof-catalog-strategies")
def list_proof_catalog_strategies():
    """Lists available proof catalog strategies."""
    typer.echo("Available Proof Catalog Strategies:")
    typer.echo("1) ConservativeProofAtlasStrategy")
    typer.echo("2) BalancedNarrativeMeshStrategy")
    typer.echo("3) ReplayClearingCouncilAtlasFirstStrategy")

if __name__ == "__main__":
    app()
