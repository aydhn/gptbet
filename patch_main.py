import re

with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

# Add import
import_str = "from src.sports_signal_bot.cli_continuity_arbitration_hardening import app as continuity_arbitration_hardening_app\n"
if "from src.sports_signal_bot.cli_continuity_arbitration_hardening" not in content:
    content = content.replace(
        "from src.sports_signal_bot.cli_planetary_federation_hardening import app as planetary_federation_hardening_app\n",
        "from src.sports_signal_bot.cli_planetary_federation_hardening import app as planetary_federation_hardening_app\n" + import_str
    )

# Add Typer subcommand
typer_str = "app.add_typer(continuity_arbitration_hardening_app, name=\"continuity-arbitration-hardening\", help=\"Post-100 Hardening Pack 18: Continuity Arbitration Hardening\")\n"
if "continuity-arbitration-hardening" not in content:
    content = content.replace(
        "app.add_typer(continuity_verification_hardening_app, name=\"continuity-verification-hardening\", help=\"Post-100 Hardening Pack 17: Continuity Verification Hardening\")\n",
        "app.add_typer(continuity_verification_hardening_app, name=\"continuity-verification-hardening\", help=\"Post-100 Hardening Pack 17: Continuity Verification Hardening\")\n" + typer_str
    )

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
