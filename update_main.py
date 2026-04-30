import sys

with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

if "from .stable_adoption.cli import app as stable_adoption_app" not in content:
    content = content.replace("from .handoff.cli import app as handoff_app", "from .handoff.cli import app as handoff_app\nfrom .stable_adoption.cli import app as stable_adoption_app")
    content = content.replace("app.add_typer(handoff_app, name=\"handoff\", help=\"Phase 48 Candidate-to-Release Handoff\")", "app.add_typer(handoff_app, name=\"handoff\", help=\"Phase 48 Candidate-to-Release Handoff\")\napp.add_typer(stable_adoption_app, name=\"stable-adoption\", help=\"Phase 49 Staged Stable Adoption\")")

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
