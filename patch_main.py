import re

with open('src/sports_signal_bot/main.py', 'r') as f:
    content = f.read()

# Add import
if 'from .cli_governance_fabric import app as governance_fabric_app' not in content:
    content = content.replace(
        'from .cli_conformance import app as conformance_app',
        'from .cli_conformance import app as conformance_app\nfrom .cli_governance_fabric import app as governance_fabric_app'
    )

# Add sub-app
if 'app.add_typer(governance_fabric_app, name="governance-fabric")' not in content:
    content = content.replace(
        'app.add_typer(conformance_app, name="conformance")',
        'app.add_typer(conformance_app, name="conformance")\napp.add_typer(governance_fabric_app, name="governance-fabric")'
    )

with open('src/sports_signal_bot/main.py', 'w') as f:
    f.write(content)

