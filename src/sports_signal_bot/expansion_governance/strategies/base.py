from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..contracts import (
    ExpansionControlStateRecord, ExpansionBudgetRecord, ExpansionPressureRecord,
    CrossCohortConflictRecord, BreakerEvaluationRecord, ExpansionCouncilRecord,
    ControlTowerSummaryRecord, ExpansionGovernanceManifest,
    ManifestInputRecord
)
from ..council import build_expansion_council_packet, aggregate_expansion_council_decision
from ..control_tower import ExpansionControlTowerBuilder
import uuid

class BaseExpansionGovernanceStrategy(ABC):
    """Base class for Expansion Governance strategies."""

    @abstractmethod
    def evaluate_state(self, metrics: Dict[str, Any]) -> ExpansionGovernanceManifest:
        """Evaluates global metrics and returns a complete governance manifest."""
        pass

    def _build_manifest(
        self,
        input_record: ManifestInputRecord
    ) -> ExpansionGovernanceManifest:

        packet = build_expansion_council_packet(
            input_record.state,
            input_record.budgets,
            input_record.pressure,
            input_record.conflicts,
            input_record.breakers
        )
        decision = aggregate_expansion_council_decision(packet)

        summary = ExpansionControlTowerBuilder.build_summary(
            input_record.state,
            input_record.budgets,
            input_record.pressure,
            input_record.breakers,
            decision
        )

        return ExpansionGovernanceManifest(
            manifest_id=f"man_{uuid.uuid4().hex[:8]}",
            control_state=input_record.state,
            council_decision=decision,
            control_tower_summary=summary
        )
