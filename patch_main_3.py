import sys

with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == 'if __name__ == "__main__":':
        new_lines.append('app.add_typer(quality_app, name="quality", help="Quality Engineering & Testing commands")\n')
    new_lines.append(line)

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.writelines(new_lines)
