with open("sports_signal_bot/src/sports_signal_bot/data/ingestion/orchestrator.py", "r") as f:
    content = f.read()

content = content.replace("from sports_signal_bot.data.providers.base import (BaseFixtureProvider,\n                                                     BaseOddsProvider,\n                                                     BaseProvider,\n                                                     BaseStatsProvider)", "#")
content = content.replace("from sports_signal_bot.data.providers.base import (BaseFixtureProvider,", "#")

with open("sports_signal_bot/src/sports_signal_bot/data/ingestion/orchestrator.py", "w") as f:
    f.write(content)
