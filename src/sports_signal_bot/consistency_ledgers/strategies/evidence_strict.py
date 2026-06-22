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


class EvidenceClearerStrictStrategy(BaseConsistencyLedgerStrategy):
    def __init__(self):
        super().__init__(name="evidence_clearer_strict_strategy")

    def apply_clearing_rules(
        self, clearer: EvidenceExchangeClearerRecord
    ) -> EvidenceExchangeClearerRecord:
        clearer.warnings.append(
            "Evidence-Strict: Evidence completeness and scope compatibility very strict"
        )
        clearer.warnings.append(
            "Evidence-Strict: Weak matches fast-tracked to review_only/no_safe"
        )
        return clearer
