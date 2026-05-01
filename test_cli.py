from typer.testing import CliRunner
from sports_signal_bot.main import app

runner = CliRunner()

def test_witness_mesh_pass():
    result = runner.invoke(app, ["witness-mesh", "run-witness-mesh-pass"])
    assert result.exit_code == 0
    assert "Starting Witness Mesh Pass" in result.stdout
    assert "Built Mesh with" in result.stdout

def test_preview_readiness():
    result = runner.invoke(app, ["witness-mesh", "preview-public-style-readiness"])
    assert result.exit_code == 0
    assert "Status: " in result.stdout
