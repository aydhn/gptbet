with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

content = content.replace(
    'app.add_typer(streaming_app, name="streaming-discovery")',
    'app.add_typer(streaming_app, name="streaming-discovery")\n\ntry:\n    from src.sports_signal_bot.resilience_fabric.cli import app as resilience_app\n    app.add_typer(resilience_app)\nexcept ImportError:\n    pass\n'
)

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
