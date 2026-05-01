1. **Create Contracts**: Define the Pydantic models for ExternalAuditRequestRecord, ExternalAuditResponseRecord, WitnessReputationRecord, etc.
2. **Implement Adapters**: Create abstract and concrete adapters for `file_packet_exchange_adapter`, `signed_json_exchange_adapter`, `audit_snapshot_exchange_adapter`, `notarization_hook_adapter`, `external_verifier_placeholder_adapter`, `witness_statement_exchange_adapter`.
3. **Implement Packets**: Safe packet building (`build_safe_exchange_packet`, `redact_exchange_payload`, etc.).
4. **Implement Response Ingestion**: Verification, schema validation, quarantine logic.
5. **Implement Notarization Hook**: NotaryProviderRecord, NotarizationDigestRecord, and helper functions to request/verify notarization.
6. **Implement Witness Reputation Model**: Scoring, adjustment, signal tracking.
7. **Implement Challenge Triage/Routing**: Priority scoring, responder suggesting, marketplace-like setup.
8. **Implement Findings Mapping**: Convert external findings to local decisions.
9. **Implement Exchange Readiness**: Public-style readiness scoring.
10. **Implement Strategies**: Base, Conservative, Balanced, QuarantineHeavy, NotarizationFirst, ReputationAware.
11. **Update Configs & Tests**: Add `configs/external_audit_exchange/*.yaml` and `tests/external_audit_exchange/test_*.py`.
12. **Add CLI Commands**: Add commands to `src/sports_signal_bot/main.py`.
13. **Update Docs**: Add `docs/external_audit_exchange_architecture.md`, `docs/operators/notarization_and_external_review_guide.md`, etc.
14. **Pre-commit Checks**: Run pre_commit_instructions to ensure all checks pass.
