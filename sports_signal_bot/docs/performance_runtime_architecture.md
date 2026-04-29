# Performance & Runtime Architecture

## Why Performance Optimization After Governance/Release?
Building a performance layer only makes sense when data models, features, schemas, and releases are stable and deterministic. We use performance engineering to speed up our workflow, reduce latency, and prevent redundant computations.

## Cache Taxonomy
- Data Cache
- Normalized Data Cache
- Feature Cache
- Model Artifact Load Cache
- Manifest/Catalog Cache
- Inference Intermediate Cache
- Release/Compatibility Lookup Cache
- Summary/Report Cache

## Incremental Recompute Philosophy
Instead of fully rebuilding our state from scratch, we identify the exact changeset (e.g., new fixtures, new odds) and perform partial execution or window replacement. This ensures precision without overhead.

## Lazy Loading Strategy
Metadata is loaded first. The full payload is only loaded on demand (deferred). This drastically cuts memory footprints when scanning catalogs or histories.

## Timing and Bottleneck Reporting
Every step in the pipeline can be timed. Bottlenecks (longest steps, heaviest cache usages) are reported automatically at the end of runs.

## Cleanup and Cache Health
Cache TTL, size limits, and invalidation rules keep the cache from growing indefinitely and from serving stale results.

## Future Extension Path
- Remote Cache
- Parquet Optimization
- Async Workers
- Distributed Execution
