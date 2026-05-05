from sports_signal_bot.consistency_ledgers.strategies.base import BaseConsistencyLedgerStrategy
from sports_signal_bot.consistency_ledgers.contracts import (
    AlignmentCompilerFederationRecord,
    DisputeTribunalMeshRecord,
    EvidenceExchangeClearerRecord,
    SovereignGovernanceConsistencyLedgerRecord,
    HealthStatus
)

class SovereigntyDominantConsistencyStrategy(BaseConsistencyLedgerStrategy):
    def __init__(self):
        super().__init__(name="sovereignty_dominant_consistency_strategy")

    def apply_federation_rules(self, federation: AlignmentCompilerFederationRecord) -> AlignmentCompilerFederationRecord:
        federation.warnings.append("Sovereignty-Dominant: Alignment outputs fast-tracked to cap")
        return federation

    def apply_mesh_rules(self, mesh: DisputeTribunalMeshRecord) -> DisputeTribunalMeshRecord:
        mesh.warnings.append("Sovereignty-Dominant: Mesh routes fast-tracked to cap")
        return mesh

    def apply_clearing_rules(self, clearer: EvidenceExchangeClearerRecord) -> EvidenceExchangeClearerRecord:
        clearer.warnings.append("Sovereignty-Dominant: Clearing outputs fast-tracked to cap")
        return clearer

    def apply_ledger_rules(self, ledger: SovereignGovernanceConsistencyLedgerRecord) -> SovereignGovernanceConsistencyLedgerRecord:
        ledger.warnings.append("Sovereignty-Dominant: Ledger statuses fast-tracked to cap")
        return ledger
