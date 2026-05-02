import os

files_to_patch = [
    "src/sports_signal_bot/resilience_fabric/swarms.py",
    "src/sports_signal_bot/resilience_fabric/game_day.py"
]

for file in files_to_patch:
    with open(file, "r") as f:
        content = f.read()

    if "datetime.UTC" in content:
        content = content.replace("datetime.now(datetime.UTC)", "datetime.utcnow()")

    with open(file, "w") as f:
        f.write(content)
