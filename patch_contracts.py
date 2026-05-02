with open("src/sports_signal_bot/resilience_fabric/contracts.py", "r") as f:
    content = f.read()

content = content.replace(
    'sequence_hint: Optional[int]',
    'sequence_hint: Optional[int] = None'
).replace(
    'freshness_hint: Optional[str]',
    'freshness_hint: Optional[str] = None'
).replace(
    'integrity_hint: Optional[str]',
    'integrity_hint: Optional[str] = None'
)

with open("src/sports_signal_bot/resilience_fabric/contracts.py", "w") as f:
    f.write(content)
