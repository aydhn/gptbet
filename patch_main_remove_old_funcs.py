import re
with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

# remove ingest_samples provider references
content = re.sub(r'def _load_provider_config.*?def', 'def', content, flags=re.DOTALL)

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
