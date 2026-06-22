from typing import Any, Dict, List

from sports_signal_bot.consistency_ledgers.contracts import (
    AlignmentCompilerFederationRecord,
    DisputeTribunalMeshRecord,
    EvidenceExchangeClearerRecord,
    SovereignGovernanceConsistencyLedgerRecord,
)


class BaseConsistencyLedgerStrategy:
    def __init__(self, name: str):
        self.name = name

    def apply_federation_rules(
        self, federation: AlignmentCompilerFederationRecord
    ) -> AlignmentCompilerFederationRecord:
        return federation

    def apply_mesh_rules(
        self, mesh: DisputeTribunalMeshRecord
    ) -> DisputeTribunalMeshRecord:
        return mesh

    def apply_clearing_rules(
        self, clearer: EvidenceExchangeClearerRecord
    ) -> EvidenceExchangeClearerRecord:
        return clearer

    def apply_ledger_rules(
        self, ledger: SovereignGovernanceConsistencyLedgerRecord
    ) -> SovereignGovernanceConsistencyLedgerRecord:
        return ledger
