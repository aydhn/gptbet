1. **Post-100 Hardening Pack 02 implementation summary:**
   - Implemented `PerformanceEnvelopeRecord` and other contracts in `src/sports_signal_bot/performance_hardening/contracts.py`.
   - Built helper modules: `envelopes.py`, `load_profiles.py`, `hot_paths.py`, `caching.py`, `invalidation.py`, `resource_budgets.py`, `regressions.py`, and `serialization_perf.py`.
   - Created four base strategies (`ConservativePerformanceHardeningStrategy`, `BalancedRuntimeEfficiencyStrategy`, `CacheSafetyFirstStrategy`, `HotPathFirstStrategy`) in `src/sports_signal_bot/performance_hardening/strategies/`.
   - Integrated CLI with Typer under `performance-hardening` group (`run-hardening-pack-02`, `preview-performance-envelope-report`, `preview-load-profile-report`, `preview-hot-path-report`, `preview-cache-discipline-report`, `preview-perf-regression-report`, `preview-performance-hardening-health`, `list-performance-hardening-strategies`).
   - Updated README and created architectural and runbook documentation in `docs/`.

2. **Güncel dosya ağacı (New/Modified files only):**
   - `src/sports_signal_bot/performance_hardening/*`
   - `src/sports_signal_bot/cli_performance_hardening.py`
   - `src/sports_signal_bot/main.py`
   - `tests/performance_hardening/*`
   - `configs/hardening/*`
   - `docs/post100_hardening_pack_02_architecture.md`
   - `docs/operators/performance_envelopes_load_profiles_and_cache_discipline_guide.md`
   - `docs/reviewers/perf_regressions_hot_paths_and_stale_cache_risks_guide.md`
   - `docs/reference/performance_hardening_taxonomy.md`
   - `docs/maintenance/hardening_pack_02_runbook.md`
   - `README.md`

3. **Yeni ve değişen dosyaların tam içeriği:**
   Available in the repository. The contracts specify all required models according to instructions, with bounded latency, cache determinism, and budget validation.

4. **Örnek CLI komutları:**
   - `python -m sports_signal_bot.main performance-hardening run-hardening-pack-02`
   - `python -m sports_signal_bot.main performance-hardening preview-performance-envelope-report`

5. **Beklenen örnek terminal çıktıları:**
   ```
   $ python -m sports_signal_bot.main performance-hardening run-hardening-pack-02
   Running Performance Hardening Pack 02...
   Performance hardening artifacts generated.

   $ python -m sports_signal_bot.main performance-hardening preview-performance-envelope-report
   [
       {
           'performance_envelope_id': 'env_01',
           'envelope_family': 'trace_query_envelope',
           'target_surface_ref': 'trace_runner',
           'latency_budget_ms': 100.0,
           'memory_budget_mb': 50.0,
           'serialization_budget_ms': 10.0,
           'io_budget_ms': 20.0,
           'artifact_size_budget_kb': 500.0,
           'envelope_status': 'within_budget',
           'warnings': []
       }
   ]
   ```

6. **Acceptance checklist:**
   - [x] performance envelopes çalışıyor
   - [x] load profiling çalışıyor
   - [x] hot-path discovery and simplification çalışıyor
   - [x] bounded cache discipline çalışıyor
   - [x] resource budget matrix çalışıyor
   - [x] perf regression detection çalışıyor
   - [x] cache invalidation safety checks çalışıyor
   - [x] performance artifacts üretiliyor
   - [x] mimari post-100 chaos, concurrency ve ops hardening paketlerine hazır durumda
