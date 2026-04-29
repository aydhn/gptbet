with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "help=\"Provider to use\")," in line:
        continue
    new_lines.append(line)

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.writelines(new_lines)
