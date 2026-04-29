import sys

with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "app.add_typer(quality_app" in line and "if __name__" not in line:
        continue # remove old one
    new_lines.append(line)

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.writelines(new_lines)
