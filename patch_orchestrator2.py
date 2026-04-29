import re
with open("sports_signal_bot/src/sports_signal_bot/data/ingestion/orchestrator.py", "r") as f:
    content = f.read()

content = content.replace("BaseFixtureProvider", "Any")
content = content.replace("BaseOddsProvider", "Any")
content = content.replace("BaseProvider", "Any")
content = content.replace("BaseStatsProvider", "Any")

with open("sports_signal_bot/src/sports_signal_bot/data/ingestion/orchestrator.py", "w") as f:
    f.write(content)
