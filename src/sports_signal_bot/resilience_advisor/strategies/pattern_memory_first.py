from typing import Dict, Any
import uuid
from .base import BaseResilienceAdvisorStrategy
from ..contracts import AdvisoryRecommendationRecord, RemediationPlaybookRecord, RecoveryOrchestrationPlanRecord
from ..matching import find_relevant_failure_patterns
from ..synthesis import synthesize_remediation_playbook
from ..orchestration import build_recovery_orchestration_plan
from ..confidence import compute_advisory_confidence
from ..memory import FailurePatternMemory

class PatternMemoryFirstStrategy(BaseResilienceAdvisorStrategy):
    def __init__(self, memory: FailurePatternMemory):
        self.memory = memory

    def generate_playbook(self, incident_signals: Dict[str, Any]) -> RemediationPlaybookRecord:
        patterns = self.memory.get_all_patterns()
        matches = find_relevant_failure_patterns(patterns, incident_signals)
        return synthesize_remediation_playbook(matches, incident_signals)

    def generate_plan(self, playbook: RemediationPlaybookRecord, incident_ref: str) -> RecoveryOrchestrationPlanRecord:
        return build_recovery_orchestration_plan(playbook, incident_ref)

    def synthesize_advice(self, incident_signals: Dict[str, Any]) -> AdvisoryRecommendationRecord:
        patterns = self.memory.get_all_patterns()
        matches = find_relevant_failure_patterns(patterns, incident_signals)

        if not matches:
             return AdvisoryRecommendationRecord(
                recommendation_id=f"rec_{uuid.uuid4().hex[:8]}",
                decision_type="no_safe_advice",
                plan_ref=None,
                confidence=compute_advisory_confidence([], RemediationPlaybookRecord(playbook_id="", playbook_family="", target_incident_family="", synthesized_from_pattern_refs=[], steps=[], prerequisites=[], risk_notes=[], rollback_notes=[], expected_signals=[])),
                why_this_pattern_match="No historical pattern found.",
                remaining_risks=["unknown_failure"]
            )

        playbook = self.generate_playbook(incident_signals)
        plan = self.generate_plan(playbook, incident_signals.get("incident_ref", "unknown"))
        confidence = compute_advisory_confidence(matches, playbook)

        return AdvisoryRecommendationRecord(
            recommendation_id=f"rec_{uuid.uuid4().hex[:8]}",
            decision_type="recommend_playbook",
            plan_ref=plan.plan_id,
            confidence=confidence,
            why_this_pattern_match="Strong historical pattern match.",
            remaining_risks=["pattern_drift"]
        )
