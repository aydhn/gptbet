from sports_signal_bot.consistency_ledgers.contracts import (
    AlignmentCompilerFederationRecord,
    DisputeTribunalMeshRecord,
    EvidenceExchangeClearerRecord,
    HealthStatus,
    SovereignGovernanceConsistencyLedgerRecord,
)
from sports_signal_bot.consistency_ledgers.strategies.base import (
    BaseConsistencyLedgerStrategy,
)


class ContextConsistencyFirstStrategy(BaseConsistencyLedgerStrategy):
    def __init__(self):
        super().__init__(name="context_consistency_first_strategy")

    def apply_federation_rules(
        self, federation: AlignmentCompilerFederationRecord
    ) -> AlignmentCompilerFederationRecord:
        federation.warnings.append(
            "Context-First: Weak evidence fast-tracked to review_only/no_safe"
        )
        return federation

    def apply_mesh_rules(
        self, mesh: DisputeTribunalMeshRecord
    ) -> DisputeTribunalMeshRecord:
        mesh.warnings.append("Context-First: Tribunal caps highly visible")
        return mesh

    def apply_clearing_rules(
        self, clearer: EvidenceExchangeClearerRecord
    ) -> EvidenceExchangeClearerRecord:
        clearer.warnings.append(
            "Context-First: Weak evidence fast-tracked to review_only/no_safe"
        )
        return clearer

    def apply_ledger_rules(
        self, ledger: SovereignGovernanceConsistencyLedgerRecord
    ) -> SovereignGovernanceConsistencyLedgerRecord:
        ledger.warnings.append("Context-First: Ledger caps highly visible")
        return ledger
