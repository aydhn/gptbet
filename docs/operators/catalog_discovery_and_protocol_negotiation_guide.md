# Catalog Discovery and Protocol Negotiation Guide

## Running Discovery
Use the CLI to run discovery passes:
```bash
python -m sports_signal_bot.main ecosystem-discovery run-ecosystem-discovery-pass
```

## Negotiation
The system will automatically attempt to negotiate a protocol subset between what the verifier offers and what the client requires. It will always default to a safe subset.
