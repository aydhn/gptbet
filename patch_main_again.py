with open("src/sports_signal_bot/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "from src.sports_signal_bot.cli_planetary_federation_hardening import app as planetary_federation_hardening_app" in line:
        new_lines.append(line)
        new_lines.append("from src.sports_signal_bot.cli_continuity_arbitration_hardening import app as continuity_arbitration_hardening_app\n")
    else:
        new_lines.append(line)

# Since we previously used string replace that failed to inject the import, we'll try again and clean up the file
content = "".join(new_lines)
with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
