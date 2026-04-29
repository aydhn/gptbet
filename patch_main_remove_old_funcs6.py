with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

import re
# Remove the `if __name__ == "__main__":` block that is above the new commands
# and put it at the very bottom
content = re.sub(r'if __name__ == "__main__":\n    app\(\)\n\n\n', '', content)

content += "\nif __name__ == '__main__':\n    app()\n"

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
