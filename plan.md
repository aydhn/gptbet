1. **Define Constants and Contracts (`contracts.py`)**
   - Write `AssuranceExchangePacketRecord`, `FederatedRegistryRecord`, `NotarizedPromotionEnvelopeRecord`, `ClaimTranslationRecord`, `CrossSystemReplayRecord` to `src/sports_signal_bot/assurance_exchange/contracts.py`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/contracts.py`.

2. **Implement Registries and Federation Core (`registries.py`, `federation.py`)**
   - Write `register_federated_registry(...)` and `validate_registry_capabilities(...)` to `src/sports_signal_bot/assurance_exchange/registries.py`.
   - Write `build_registry_federation_link(...)` to `src/sports_signal_bot/assurance_exchange/federation.py`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/registries.py src/sports_signal_bot/assurance_exchange/federation.py`.

3. **Implement Packet Exchange and Compatibility (`packets.py`, `compatibility.py`)**
   - Write `build_exchange_packet(...)` and `validate_packet_integrity(...)` to `src/sports_signal_bot/assurance_exchange/packets.py`.
   - Write `build_compatibility_matrix(...)` and `evaluate_registry_compatibility(...)` to `src/sports_signal_bot/assurance_exchange/compatibility.py`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/packets.py src/sports_signal_bot/assurance_exchange/compatibility.py`.

4. **Implement Translation and Replay (`translations.py`, `replay.py`)**
   - Write `translate_assurance_claim(...)` and validation helpers to `src/sports_signal_bot/assurance_exchange/translations.py`.
   - Write `build_cross_system_replay_context(...)` and `replay_external_assurance_packet(...)` to `src/sports_signal_bot/assurance_exchange/replay.py`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/translations.py src/sports_signal_bot/assurance_exchange/replay.py`.

5. **Implement Notarization and Quarantine (`notarized_envelopes.py`, `quarantine.py`)**
   - Write `build_notarized_promotion_envelope(...)` and `verify_notarized_envelope(...)` to `src/sports_signal_bot/assurance_exchange/notarized_envelopes.py`.
   - Write `quarantine_assurance_packet(...)` and `decide_quarantine_release(...)` to `src/sports_signal_bot/assurance_exchange/quarantine.py`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/notarized_envelopes.py src/sports_signal_bot/assurance_exchange/quarantine.py`.

6. **Implement Sync and Integration (`sync.py`, `integration.py`)**
   - Write `build_registry_snapshot(...)`, `export_registry_snapshot(...)` to `src/sports_signal_bot/assurance_exchange/sync.py`.
   - Write `run_interop_verification(...)` to `src/sports_signal_bot/assurance_exchange/integration.py`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/sync.py src/sports_signal_bot/assurance_exchange/integration.py`.

7. **Implement Reporting and Manifests (`reporting.py`, `manifests.py`)**
   - Write `build_assurance_exchange_summary(...)` and KPI logic to `src/sports_signal_bot/assurance_exchange/reporting.py`.
   - Write `build_assurance_exchange_manifest(...)` logic to `src/sports_signal_bot/assurance_exchange/manifests.py`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/reporting.py src/sports_signal_bot/assurance_exchange/manifests.py`.

8. **Implement Diagnostics, Evidence, Utilities (`diagnostics.py`, `evidence.py`, `utils.py`)**
   - Write `InteropWarningRecord` and `AssuranceExchangeAuditRecord` models to `src/sports_signal_bot/assurance_exchange/diagnostics.py`.
   - Write `validate_proof_portability(...)` and `export_portable_proof_bundle(...)` to `src/sports_signal_bot/assurance_exchange/evidence.py`.
   - Write `load_yaml_config(...)` and `get_utc_now(...)` helpers to `src/sports_signal_bot/assurance_exchange/utils.py`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/diagnostics.py src/sports_signal_bot/assurance_exchange/evidence.py src/sports_signal_bot/assurance_exchange/utils.py`.

9. **Implement Assurance Exchange Strategies Part 1 (`strategies/`)**
   - Write `base.py`, `conservative.py`, `balanced_registry_federation.py` in `src/sports_signal_bot/assurance_exchange/strategies/`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/strategies/base.py src/sports_signal_bot/assurance_exchange/strategies/conservative.py src/sports_signal_bot/assurance_exchange/strategies/balanced_registry_federation.py`.

10. **Implement Assurance Exchange Strategies Part 2 (`strategies/`)**
   - Write `quarantine_heavy.py`, `notarized_envelope_first.py`, `replay_strict.py` in `src/sports_signal_bot/assurance_exchange/strategies/`.
   - Verify syntax with `python -m py_compile src/sports_signal_bot/assurance_exchange/strategies/quarantine_heavy.py src/sports_signal_bot/assurance_exchange/strategies/notarized_envelope_first.py src/sports_signal_bot/assurance_exchange/strategies/replay_strict.py`.
   - Write `__init__.py` for strategies and module.

11. **Implement CLI and Hook it Up (`cli.py`, `main.py`)**
   - Write Typer app with commands `run-assurance-exchange-pass`, `preview-federated-registries`, `preview-assurance-exchange-packets`, `preview-compatibility-matrices`, `preview-cross-system-replay`, `preview-notarized-promotion-envelopes`, `list-assurance-exchange-strategies` to `src/sports_signal_bot/assurance_exchange/cli.py`.
   - Update `src/sports_signal_bot/main.py` using sed to add the import `from .assurance_exchange.cli import app as assurance_exchange_app` and `app.add_typer(assurance_exchange_app, name="assurance-exchange")`.
   - Verify with `python -m sports_signal_bot.main --help`.

12. **Add Tests Part 1**
   - Write `test_registry_federation_links.py`, `test_exchange_packet_integrity.py`, `test_claim_translation_safety.py` to `tests/assurance_exchange/`.
   - Verify with `ls -la tests/assurance_exchange/`.

13. **Add Tests Part 2**
   - Write `test_compatibility_matrix.py`, `test_cross_system_replay.py`, `test_notarized_promotion_envelopes.py`, `test_quarantine_paths.py` to `tests/assurance_exchange/`.
   - Verify with `ls -la tests/assurance_exchange/`.

14. **Add Tests Part 3**
   - Write `test_snapshot_sync_and_supersession.py`, `test_interop_verification_summaries.py`, `test_reporting_hooks.py`, `test_assurance_exchange_manifest.py` to `tests/assurance_exchange/`.
   - Verify with `ls -la tests/assurance_exchange/`.

15. **Update Documentation (`docs/`)**
   - Write `docs/assurance_exchange_and_registry_federation_architecture.md`, `docs/operators/federated_registry_and_exchange_guide.md`.
   - Verify with `ls -la docs/`.

16. **Update Documentation (`docs/` and `README.md`)**
   - Write `docs/reviewers/claim_translation_and_replay_guide.md`, `docs/reference/assurance_interoperability_taxonomy.md`, `docs/maintenance/assurance_exchange_runbook.md`.
   - Append section to `README.md`.
   - Verify with `ls -la docs/`.

17. **Run Tests**
   - Run the entire test suite `pytest tests/assurance_exchange/` to verify logic.

18. **Complete Pre-commit Steps**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
