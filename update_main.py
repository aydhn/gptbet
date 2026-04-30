import sys

with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

if "from sports_signal_bot.adjudication.cli import app as adjudication_app" not in content:
    content += "\nfrom sports_signal_bot.adjudication.cli import app as adjudication_app\n"
    content += "app.add_typer(adjudication_app, name=\"adjudication\")\n"

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
