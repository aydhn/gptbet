from sports_signal_bot.evidence.builders.base import BaseEvidenceBuilder
from sports_signal_bot.evidence.contracts import EvidenceBundleRecord

class DecisionEvidenceBuilder(BaseEvidenceBuilder):
    def __init__(self, target_entity_id: str, audience_profile: str):
        super().__init__(target_entity_type="decision", target_entity_id=target_entity_id, audience_profile=audience_profile)

    def build(self) -> EvidenceBundleRecord:
        bundle = super().build()
        bundle.bundle_type = "decision_evidence"
        return bundle
