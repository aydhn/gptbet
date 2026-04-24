# Data Architecture

## Provider-First Approach
The ingestion pipeline doesn't care *where* data comes from. All data sources implement `BaseFixtureProvider`, `BaseOddsProvider`, etc. This isolates downstream logic from API schema changes.

## Canonical Schema
We parse various raw provider schemas into a highly disciplined canonical Pydantic model (`CanonicalEventRecord`, `CanonicalOddsRecord`). All downstream feature generation and model training only interact with the canonical format.

## Quality Gate
Before reaching the processed layer, data passes through validators:
- Required fields
- Datetime parsing to UTC
- Valid match-ups (Home != Away)
- Sensible odds (> 1.0)
- Deduplication

## Manifest and Lineage
Every ingestion run creates a `ManifestRecord` containing metrics (valid/invalid counts, duplications) and traces back the raw and processed output paths. This provides perfect data lineage.

## Why File/Mock First?
It establishes the pipeline logic and tests the schemas without being distracted by network API quirks. It lets us write all the downstream logic (validation, models, backtesting) without being blocked by API access constraints.

## Future: Multi-Source Merge
Because we enforce canonical schemas and use entity resolution (alias mapping), future integrations of multiple free APIs can be merged seamlessly.
