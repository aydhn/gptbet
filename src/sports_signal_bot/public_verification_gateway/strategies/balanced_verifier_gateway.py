from typing import Dict, List
from .base import BasePublicationStrategy

class BalancedVerifierGatewayStrategy(BasePublicationStrategy):
    """
    Balanced verifier gateway strategy.
    - Balances public_minimal and external_verifier
    - Moderate quarantine threshold
    """

    def get_default_profile(self) -> str:
        return "public_verifier"

    def allowed_profiles(self) -> List[str]:
        return ["public_minimal", "public_verifier", "external_auditor", "internal_publication_preview"]

    def evaluate_quarantine_threshold(self, malformed_intake_rate: float) -> bool:
        return malformed_intake_rate > 0.20
