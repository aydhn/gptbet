import os

files_to_patch = [
    "src/sports_signal_bot/resilience_fabric/swarms.py",
    "src/sports_signal_bot/resilience_fabric/game_day.py",
    "src/sports_signal_bot/resilience_fabric/contracts.py"
]

for file in files_to_patch:
    with open(file, "r") as f:
        content = f.read()

    if "datetime.utcnow()" in content:
        content = content.replace("datetime.utcnow()", "datetime.now(datetime.UTC)")
    if "from datetime import datetime" in content and "timezone" not in content and "datetime.UTC" in content:
        pass # datetime.UTC is available in python 3.11+

    with open(file, "w") as f:
        f.write(content)
