with open("src/sports_signal_bot/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
insert_idx = -1
for i, line in enumerate(lines):
    if line.strip() == "if __name__ == \"__main__\":":
        insert_idx = i
        break

if insert_idx != -1:
    new_lines = lines[:insert_idx]
    new_lines.extend([
        "from sports_signal_bot.cli_hardening import app as hardening_app\n",
        "app.add_typer(hardening_app, name=\"hardening\", help=\"Post-100 Hardening Pack 01 Commands\")\n",
        "from sports_signal_bot.regional_hardening_cli import app as regional_hardening_app\n",
        "app.add_typer(regional_hardening_app, name=\"regional-hardening\", help=\"Post-100 Hardening Pack 08: Regional Hardening\")\n",
        "if __name__ == \"__main__\":\n",
        "    app()\n"
    ])

    with open("src/sports_signal_bot/main.py", "w") as f:
        f.writelines(new_lines)
