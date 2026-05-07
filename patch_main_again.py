import re

with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

import_str = "from sports_signal_bot.cli_global_hardening import app as global_hardening_app\n"
add_str = "app.add_typer(global_hardening_app, name=\"global-hardening\", help=\"Post-100 Hardening Pack 11: Global Hardening\")\n"

if "global_hardening_app" not in content:
    content += "\n" + import_str + add_str

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
