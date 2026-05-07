from typer.testing import CliRunner
from src.sports_signal_bot.main import app
import json

runner = CliRunner()

def test_bootstrap_dry_run():
    result = runner.invoke(app, ["deploy", "bootstrap", "--profile", "research_local", "--dry-run"])
    assert result.exit_code == 0
    assert "Bootstrapping workspace" in result.stdout
    assert "init_repo_default_workspace" in result.stdout

def test_doctor():
    result = runner.invoke(app, ["deploy", "run-doctor"])
    assert result.exit_code == 0
    assert "Running environment doctor" in result.stdout
    assert "System is healthy." in result.stdout

def test_preview_layout():
    result = runner.invoke(app, ["deploy", "preview-layout"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert "workspace_root" in data
    assert "config_root" in data

def test_backup_and_restore():
    result = runner.invoke(app, ["deploy", "create-backup-cmd", "--btype", "config_and_state_backup"])
    assert result.exit_code == 0
    assert "Backup complete" in result.stdout
    # Extract ID
    # This is a bit tricky, let's just assert success for now, or find the ID
    output = result.stdout.strip()
    manifest_id = output.split("Manifest: ")[-1].strip()

    result_restore = runner.invoke(app, ["deploy", "restore-backup", manifest_id, "--dry-run"])
    assert result_restore.exit_code == 0
    assert "dry-run success" in result_restore.stdout
    assert "configs" in result_restore.stdout

def test_upgrade_preflight():
    result = runner.invoke(app, ["deploy", "run-upgrade-preflight-command"])
    assert result.exit_code == 0
    data = json.loads(result.stdout.split("preflight checks...")[-1])
    assert "current_layout_version" in data
    assert "backup_recommended" in data
