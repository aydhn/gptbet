import sys

with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

import_str = """try:
    from sports_signal_bot.cli_governance_assurance import app as governance_assurance_app
    app.add_typer(governance_assurance_app, name="governance-assurance", help="Phase 90: Governance Assurance")
except ImportError as e:
    print(f"Failed to import governance assurance cli: {e}")

if __name__ == "__main__":
"""

content = content.replace('if __name__ == "__main__":\n', import_str)

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
