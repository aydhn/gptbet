# Proof Catalogs Runbook

## Daily Health Check
Run the proof catalogs health preview:
```bash
python -m sports_signal_bot.main proof-catalogs preview-proof-catalogs-health
```

## Handling Observatory Anomalies
1. Preview observatory state:
```bash
python -m sports_signal_bot.main proof-catalogs preview-mesh-observatories
```
2. If anomalies (e.g., `caveat_drop_detected`) are present, investigate the upstream mesh traffic.
3. If necessary, trigger an audit board case to review affected narratives.

## Handling Stale Proofs
Stale proofs degrade federation and audit outcomes.
1. Check the proof catalog for stale entries.
2. Instruct the upstream proof generators (e.g., replay or debt ledgers) to emit fresh proof.
3. Re-run the proof catalogs pass:
```bash
python -m sports_signal_bot.main proof-catalogs run-proof-catalogs-pass
```
