import re

with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

# Add import
import_stmt = "from .federated_governance.cli import app as federated_governance_app\n"
if "federated_governance_app" not in content:
    content = content.replace("from .expansion_governance.cli import app as expansion_governance_app",
                              "from .expansion_governance.cli import app as expansion_governance_app\n" + import_stmt)

# Add typer app
add_typer_stmt = "app.add_typer(federated_governance_app, name=\"federated-governance\", help=\"Phase 52 Federated Governance\")\n"
if "name=\"federated-governance\"" not in content:
    content = content.replace("app.add_typer(expansion_governance_app, name=\"expansion-governance\", help=\"Phase 51 Expansion Governance\")",
                              "app.add_typer(expansion_governance_app, name=\"expansion-governance\", help=\"Phase 51 Expansion Governance\")\n" + add_typer_stmt)

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
