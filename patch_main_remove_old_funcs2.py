import re
with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

# completely remove provider_healthcheck since we have preview_provider_health
content = re.sub(r'@app\.command\(\)\ndef provider_healthcheck.*?(?=@app\.command\(\)|\Z)', '', content, flags=re.DOTALL)

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
