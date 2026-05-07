with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

import_statement = "from src.sports_signal_bot.cli_continuity_arbitration_hardening import app as continuity_arbitration_hardening_app\n"
if "from src.sports_signal_bot.cli_continuity_arbitration_hardening" not in content:
    content = import_statement + content

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
