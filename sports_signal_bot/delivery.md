# Phase 32: Performance & Runtime Optimization Layer Delivery

## 1. Phase 32 Implementation Summary
A comprehensive performance and runtime optimization layer has been added to the system. This phase introduces profiling, timing, strict cache contracts (Cache Taxonomy, Invalidation, Freshness), incremental recompute strategies, and lazy loading mechanisms.

Key components:
- **Profiling & Timing**: Step profilers, `PerformanceTimer` context managers, and bottleneck reporters to measure and output execution metadata.
- **Cache Taxonomy**: Standardized cache families, policies (`no_cache`, `session_cache`, `file_cache`, `time_bounded_cache`, etc.), key generation strategies ensuring determinism.
- **Incremental Recompute**: An engine capable of comparing changeset sizes to determine whether to perform a full rebuild or an incremental window append.
- **Lazy Loading**: Deferred payload materialization structures (e.g., `LazyManifestLoader`) to only pull metadata by default and fetch the rest on-demand.
- **Strategies & Runner**: Five performance modes (`SafeDefaultPerformanceMode`, `InferenceOptimizedMode`, `BackfillOptimizedMode`, `DiagnosticsHeavyMode`, `MaintenanceCleanupMode`) integrated into a `PerformanceRunner` CLI accessible via `perf`.

## 2. Updated File Tree
The primary additions reside within `src/sports_signal_bot/performance/` and `configs/performance/`.
- `configs/performance/`: default.yaml, cache.yaml, incremental.yaml, lazy_loading.yaml, profiling.yaml, cleanup.yaml.
- `docs/performance_runtime_architecture.md`: Architecture specification.
- `src/sports_signal_bot/performance/`: contracts.py, cache_keys.py, cache_policies.py, cache_store.py, invalidation.py, incremental.py, lazy_loading.py, profiling.py, bottlenecks.py, cleanup.py, factory.py, runner.py, and the `strategies` module.
- `src/sports_signal_bot/main_performance_cli.py`: Typer CLI entrypoint.
- `src/sports_signal_bot/main.py`: Attached the performance CLI (`perf` namespace).
- `tests/test_performance_layer.py`: Comprehensive test suite for determinism and strategy execution.

## 3. Example CLI Commands
Run these commands to observe the new capabilities:
- `python -m sports_signal_bot.main perf run-performance-pass --mode inference_optimized`
- `python -m sports_signal_bot.main perf preview-cache-health`
- `python -m sports_signal_bot.main perf preview-bottlenecks`
- `python -m sports_signal_bot.main perf preview-incremental-plan --sport basketball --market moneyline`
- `python -m sports_signal_bot.main perf list-performance-modes`

## 4. Expected Terminal Output
```
Selected performance mode: inference_optimized
Step timing summary generated.
Cache hit/miss summary generated.
Incremental/full recompute decision summary generated.
Bottleneck highlights generated.
Artifact path: results/performance/performance_manifest_perf_1714392019.json
```

## 5. Acceptance Checklist
- [x] Profiling/timing infrastructure is functional (`StepProfiler`, `PerformanceTimer`).
- [x] Cache key determinism and policy layer are verified via tests.
- [x] Invalidation and freshness rules are structured.
- [x] Incremental recompute plan generation works.
- [x] Lazy loading handlers are functional (`LazyManifestLoader`).
- [x] Bottleneck and runtime summary artifacts are created correctly (`performance_manifest_perf_XXXX.json`).
- [x] CLI tools are cleanly exposed under the `perf` group.
- [x] System architecture supports distributed/remote extensions cleanly via abstraction interfaces.
