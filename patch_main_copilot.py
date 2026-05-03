import re

with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

import_stmt = "from sports_signal_bot.cli.remediation_copilot import app as copilot_app\n"

if "from sports_signal_bot.cli.remediation_copilot import app as copilot_app" not in content:
    # insert import
    content = content.replace("from sports_signal_bot.cli.resilience_advisor import app as resilience_advisor_app", "from sports_signal_bot.cli.resilience_advisor import app as resilience_advisor_app\n" + import_stmt)

    # insert add_typer
    content = content.replace("app.add_typer(resilience_advisor_app, name=\"resilience-advisor\")", "app.add_typer(resilience_advisor_app, name=\"resilience-advisor\")\napp.add_typer(copilot_app, name=\"remediation-copilot\")")

    with open("src/sports_signal_bot/main.py", "w") as f:
        f.write(content)

print("patched")
