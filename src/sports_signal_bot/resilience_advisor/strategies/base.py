from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..contracts import AdvisoryRecommendationRecord, RemediationPlaybookRecord, RecoveryOrchestrationPlanRecord

class BaseResilienceAdvisorStrategy(ABC):
    @abstractmethod
    def synthesize_advice(self, incident_signals: Dict[str, Any]) -> AdvisoryRecommendationRecord:
        pass

    @abstractmethod
    def generate_playbook(self, incident_signals: Dict[str, Any]) -> RemediationPlaybookRecord:
        pass

    @abstractmethod
    def generate_plan(self, playbook: RemediationPlaybookRecord, incident_ref: str) -> RecoveryOrchestrationPlanRecord:
        pass
