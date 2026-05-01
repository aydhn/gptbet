from typing import Dict, List
from .base import BasePublicationStrategy

class ProofRichVerifierStrategy(BasePublicationStrategy):

    def get_default_profile(self) -> str:
        return "external_auditor"

    def allowed_profiles(self) -> List[str]:
        return ["public_minimal", "public_verifier", "external_auditor", "trusted_exchange_partner"]

    def evaluate_quarantine_threshold(self, malformed_intake_rate: float) -> bool:
        return malformed_intake_rate > 0.15
