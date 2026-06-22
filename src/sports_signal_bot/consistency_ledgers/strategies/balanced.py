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


class BalancedTribunalClearingFederationStrategy(BaseConsistencyLedgerStrategy):
    def __init__(self):
        super().__init__(name="balanced_tribunal_clearing_federation_strategy")

    def apply_federation_rules(
        self, federation: AlignmentCompilerFederationRecord
    ) -> AlignmentCompilerFederationRecord:
        federation.warnings.append("Balanced: Federations are balanced")
        return federation

    def apply_mesh_rules(
        self, mesh: DisputeTribunalMeshRecord
    ) -> DisputeTribunalMeshRecord:
        mesh.warnings.append("Balanced: Meshes are balanced")
        return mesh

    def apply_clearing_rules(
        self, clearer: EvidenceExchangeClearerRecord
    ) -> EvidenceExchangeClearerRecord:
        clearer.warnings.append("Balanced: Clearers are balanced")
        return clearer

    def apply_ledger_rules(
        self, ledger: SovereignGovernanceConsistencyLedgerRecord
    ) -> SovereignGovernanceConsistencyLedgerRecord:
        ledger.warnings.append("Balanced: Ledgers are balanced, safety-first")
        return ledger
