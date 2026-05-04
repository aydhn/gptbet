# Atlas Federations, Audit Boards, Observatories & Proof Catalogs Guide

## Overview
This guide provides operational procedures for managing Phase 93 components:
1. Evidence Atlas Federations
2. Narrative Audit Boards
3. Assurance Mesh Observatories
4. Sovereign Governance Proof Catalogs

## Operations
### Evidence Atlas Federations
To preview the state of an atlas federation:
```bash
python -m sports_signal_bot.main proof-catalogs preview-atlas-federations
```

### Narrative Audit Boards
To preview the state of a narrative audit board:
```bash
python -m sports_signal_bot.main proof-catalogs preview-narrative-audit-boards
```

### Assurance Mesh Observatories
To preview the state of an assurance mesh observatory:
```bash
python -m sports_signal_bot.main proof-catalogs preview-mesh-observatories
```

### Sovereign Governance Proof Catalogs
To preview the state of a sovereign governance proof catalog:
```bash
python -m sports_signal_bot.main proof-catalogs preview-proof-catalogs
```

## Health Monitoring
To preview the overall health of proof catalogs and observatories:
```bash
python -m sports_signal_bot.main proof-catalogs preview-proof-catalogs-health
```
This checks for stale entries, anomalous mesh conditions, and verifies that no-safe boundaries and sovereignty constraints are intact.
