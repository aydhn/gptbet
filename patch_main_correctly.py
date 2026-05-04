import re

with open('src/sports_signal_bot/main.py', 'r') as f:
    content = f.read()

# Make sure we add governance fabric cli
new_cli_code = """
try:
    from sports_signal_bot.cli_governance_fabric import app as governance_fabric_app
    app.add_typer(governance_fabric_app, name="governance-fabric", help="Phase 83: Governance Fabric")
except ImportError as e:
    print(f"Failed to import governance fabric cli: {e}")
"""

if 'name="governance-fabric"' not in content:
    content = content.replace(
        'except ImportError:\n    pass',
        'except ImportError:\n    pass\n' + new_cli_code
    )

with open('src/sports_signal_bot/main.py', 'w') as f:
    f.write(content)
