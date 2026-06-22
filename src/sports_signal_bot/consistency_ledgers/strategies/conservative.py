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


class ConservativeConsistencyLedgerStrategy(BaseConsistencyLedgerStrategy):
    def __init__(self):
        super().__init__(name="conservative_consistency_ledger_strategy")

    def apply_federation_rules(
        self, federation: AlignmentCompilerFederationRecord
    ) -> AlignmentCompilerFederationRecord:
        federation.warnings.append("Conservative: Stale currentness heavily penalized")
        federation.health_status = (
            HealthStatus.DEGRADED
            if len(federation.active_link_refs) == 0
            else HealthStatus.HEALTHY
        )
        return federation

    def apply_mesh_rules(
        self, mesh: DisputeTribunalMeshRecord
    ) -> DisputeTribunalMeshRecord:
        mesh.warnings.append("Conservative: Mesh routes fast-tracked to caveated/stale")
        return mesh

    def apply_clearing_rules(
        self, clearer: EvidenceExchangeClearerRecord
    ) -> EvidenceExchangeClearerRecord:
        clearer.warnings.append(
            "Conservative: Cleared outputs fast-tracked to caveated/stale"
        )
        return clearer

    def apply_ledger_rules(
        self, ledger: SovereignGovernanceConsistencyLedgerRecord
    ) -> SovereignGovernanceConsistencyLedgerRecord:
        ledger.warnings.append("Conservative: No-safe visibility strongly prioritized")
        return ledger
