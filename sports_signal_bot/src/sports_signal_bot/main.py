import typer
from sports_signal_bot.orchestration.runner import SmokeRunner
from sports_signal_bot.config.settings import get_settings
from sports_signal_bot.core.paths import get_data_dir, get_configs_dir
from sports_signal_bot.core.random import set_global_seed

app = typer.Typer(help="Sports Signal Bot CLI")

@app.command()
def smoke_run():
    """Run a basic smoke test pipeline."""
    set_global_seed(42)
    runner = SmokeRunner()
    runner.run()

@app.command()
def show_config():
    """Display the current configuration settings."""
    settings = get_settings()
    typer.echo("Current Configuration:")
    typer.echo(settings.model_dump_json(indent=2))

@app.command()
def paths():
    """Display project paths."""
    typer.echo(f"Data Directory: {get_data_dir()}")
    typer.echo(f"Configs Directory: {get_configs_dir()}")

if __name__ == "__main__":
    app()
