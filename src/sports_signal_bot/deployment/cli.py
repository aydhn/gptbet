import typer
import json
from pathlib import Path
from .layout import resolve_workspace_root, build_deployment_layout
from .bootstrap import run_bootstrap
from .contracts import BootstrapMode, BackupType
from .doctor import run_environment_doctor
from .backup import create_backup
from .restore import run_restore
from .upgrade import run_upgrade_preflight

app = typer.Typer(help="Platform packaging and local deployment operations")

@app.command()
def bootstrap(profile: str = "research_local", dry_run: bool = False):
    typer.echo(f"Bootstrapping workspace with profile '{profile}' (dry_run={dry_run})...")
    root = resolve_workspace_root()
    plan = run_bootstrap(root, profile, BootstrapMode.INIT_REPO_DEFAULT_WORKSPACE, dry_run)
    typer.echo(json.dumps(plan, indent=2))

@app.command("run-doctor")
def run_doctor():
    typer.echo("Running environment doctor...")
    root = resolve_workspace_root()
    layout = build_deployment_layout(root)
    report = run_environment_doctor(layout)
    typer.echo(report.model_dump_json(indent=2))
    if not report.is_ready:
        typer.secho("System is NOT ready. Critical issues found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    typer.secho("System is healthy.", fg=typer.colors.GREEN)

@app.command()
def preview_layout():
    root = resolve_workspace_root()
    layout = build_deployment_layout(root)
    typer.echo(layout.model_dump_json(indent=2))

@app.command()
def create_backup_cmd(btype: BackupType = BackupType.CONFIG_AND_STATE_BACKUP):
    typer.echo(f"Creating backup of type: {btype.value}")
    root = resolve_workspace_root()
    layout = build_deployment_layout(root)
    manifest = create_backup(layout, btype)
    typer.echo(f"Backup complete. Manifest: {manifest.backup_id}")

@app.command()
def restore_backup(backup_id: str, dry_run: bool = True, force: bool = False):
    typer.echo(f"Restoring backup {backup_id} (dry_run={dry_run}, force={force})...")
    root = resolve_workspace_root()
    layout = build_deployment_layout(root)
    try:
        res = run_restore(layout, backup_id, dry_run, force)
        typer.echo(json.dumps(res, indent=2))
    except RuntimeError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)

@app.command()
def run_upgrade_preflight_command():
    typer.echo("Running upgrade preflight checks...")
    root = resolve_workspace_root()
    layout = build_deployment_layout(root)
    preflight = run_upgrade_preflight(layout)
    typer.echo(preflight.model_dump_json(indent=2))
