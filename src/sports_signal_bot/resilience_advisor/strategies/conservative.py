from typing import Dict, Any
import uuid
from .base import BaseResilienceAdvisorStrategy
from ..contracts import AdvisoryRecommendationRecord, RemediationPlaybookRecord, RecoveryOrchestrationPlanRecord
from ..matching import find_relevant_failure_patterns
from ..synthesis import synthesize_remediation_playbook
from ..orchestration import build_recovery_orchestration_plan
from ..confidence import compute_advisory_confidence
from ..memory import FailurePatternMemory

class ConservativeRecoveryAdvisorStrategy(BaseResilienceAdvisorStrategy):
    def __init__(self, memory: FailurePatternMemory):
        self.memory = memory

    def generate_playbook(self, incident_signals: Dict[str, Any]) -> RemediationPlaybookRecord:
        patterns = self.memory.get_all_patterns()
        matches = find_relevant_failure_patterns(patterns, incident_signals)
        return synthesize_remediation_playbook(matches, incident_signals)

    def generate_plan(self, playbook: RemediationPlaybookRecord, incident_ref: str) -> RecoveryOrchestrationPlanRecord:
        plan = build_recovery_orchestration_plan(playbook, incident_ref)
        plan.review_requirements.append("mandatory_quarantine_review")
        return plan

    def synthesize_advice(self, incident_signals: Dict[str, Any]) -> AdvisoryRecommendationRecord:
        playbook = self.generate_playbook(incident_signals)
        plan = self.generate_plan(playbook, incident_signals.get("incident_ref", "unknown"))
        matches = find_relevant_failure_patterns(self.memory.get_all_patterns(), incident_signals)
        confidence = compute_advisory_confidence(matches, playbook)

        # In conservative, cap confidence
        if confidence.confidence_band in ["high", "high_with_caveats"]:
            confidence.confidence_band = "moderate"

        return AdvisoryRecommendationRecord(
            recommendation_id=f"rec_{uuid.uuid4().hex[:8]}",
            decision_type="recommend_quarantine_first",
            plan_ref=plan.plan_id,
            confidence=confidence,
            why_this_pattern_match="Conservative default matches quarantine strategies",
            remaining_risks=["over_quarantine"]
        )
