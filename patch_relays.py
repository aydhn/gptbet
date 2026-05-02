with open("src/sports_signal_bot/resilience_fabric/relays.py", "r") as f:
    content = f.read()

content = content.replace(
    'return RelayEnvelopeRecord(',
    'return RelayEnvelopeRecord(\n        sequence_hint=None,\n        freshness_hint=None,\n        integrity_hint=None,'
)

with open("src/sports_signal_bot/resilience_fabric/relays.py", "w") as f:
    f.write(content)
