from typing import Dict, List
from .base import BasePublicationStrategy

class IntakeHardenedStrategy(BasePublicationStrategy):

    def get_default_profile(self) -> str:
        return "public_minimal"

    def allowed_profiles(self) -> List[str]:
        return ["public_minimal", "public_verifier"]

    def evaluate_quarantine_threshold(self, malformed_intake_rate: float) -> bool:
        # Strict quarantine for any intake anomalies
        return malformed_intake_rate > 0.01
