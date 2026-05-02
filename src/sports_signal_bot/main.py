import typer

try:
    from sports_signal_bot.streaming_discovery.cli import app as streaming_app
except ImportError:
    streaming_app = typer.Typer()

app = typer.Typer()
app.add_typer(streaming_app, name="streaming-discovery")

@app.command()
def smoke_run():
    typer.echo("Smoke run OK.")

if __name__ == "__main__":
    app()
