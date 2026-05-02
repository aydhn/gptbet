import os

files_to_patch = [
    "src/sports_signal_bot/resilience_fabric/swarms.py",
    "src/sports_signal_bot/resilience_fabric/game_day.py"
]

for file in files_to_patch:
    with open(file, "r") as f:
        content = f.read()

    if "from datetime import datetime" in content:
        content = content.replace("from datetime import datetime", "from datetime import datetime, timezone")
    if "datetime.utcnow()" in content:
        content = content.replace("datetime.utcnow()", "datetime.now(timezone.utc)")

    with open(file, "w") as f:
        f.write(content)
