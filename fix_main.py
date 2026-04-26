with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

idx = content.find('if __name__ == "__main__":')
if idx != -1:
    top = content[:idx]
    bottom = content[idx:]

    # We need to move the last parts (my append) BEFORE the if __name__ part.
    # The length of main.py is ~2200 lines

    lines = content.split('\n')
    new_lines = []

    if_idx = -1
    for i, line in enumerate(lines):
        if line.startswith('if __name__ == "__main__":'):
            if_idx = i
            break

    if if_idx != -1:
        # Check what follows
        # We find where my appended code starts: "from sports_signal_bot.backtest.runner import BacktestRunner"

        my_code_start = -1
        for i, line in enumerate(lines):
            if "from sports_signal_bot.backtest.runner import BacktestRunner" in line:
                my_code_start = i
                break

        if my_code_start != -1 and my_code_start > if_idx:
            # We must swap!

            part1 = lines[:if_idx]
            part_if = lines[if_idx:my_code_start] # Should just be the if __name__ block
            part_my_code = lines[my_code_start:]

            # wait, part_my_code also contains my second append!
            # I'll just remove the if __name__ block and put it at the very very end!

            clean_lines = [l for l in lines if not l.startswith('if __name__ == "__main__":') and not l.strip() == "app()"]
            clean_lines.append('if __name__ == "__main__":')
            clean_lines.append('    app()')

            with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f2:
                f2.write('\n'.join(clean_lines))
