import re

with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

# Add import
import_str = "from .candidate_promotion.cli import app as candidate_promotion_app\nfrom .auto_promotion.cli import app as auto_promotion_app"
content = content.replace("from .candidate_promotion.cli import app as candidate_promotion_app", import_str)

# Add typer app
typer_str = "app.add_typer(candidate_promotion_app, name=\"candidate-promotion\", help=\"Phase 45 Candidate Promotion\")\napp.add_typer(auto_promotion_app, name=\"auto-promotion\", help=\"Phase 47 Constrained Auto Promotion\")"
content = content.replace("app.add_typer(candidate_promotion_app, name=\"candidate-promotion\", help=\"Phase 45 Candidate Promotion\")", typer_str)

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
