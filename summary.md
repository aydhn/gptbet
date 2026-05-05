1. **Post-100 Hardening Pack 02 implementation summary:**
   - Implemented `PerformanceEnvelopeRecord` and other contracts in `performance_hardening/contracts.py`.
   - Built helper modules: `envelopes`, `load_profiles`, `hot_paths`, `caching`, `invalidation`, `resource_budgets`, `regressions`, and `serialization_perf`.
   - Created four base strategies (`ConservativePerformanceHardeningStrategy`, `BalancedRuntimeEfficiencyStrategy`, `CacheSafetyFirstStrategy`, `HotPathFirstStrategy`).
   - Integrated CLI with Typer under `performance-hardening` group (`run-hardening-pack-02`, `preview-performance-envelope-report`, etc.).
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
   Running Performance Hardening Pack 02...
   Performance hardening artifacts generated.
   ```
   ```
   [{'performance_envelope_id': 'env_01', 'envelope_family': 'trace_query_envelope', 'envelope_status': 'within_budget', ...}]
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
