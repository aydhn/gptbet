with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "from sports_signal_bot.data.providers.file_provider" in line:
        skip = True
    elif skip and ")" in line:
        skip = False
        continue
    elif skip:
        continue
    elif "from sports_signal_bot.data.providers.mock_provider" in line:
        skip = True
    else:
        if not skip:
            new_lines.append(line)

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.writelines(new_lines)
