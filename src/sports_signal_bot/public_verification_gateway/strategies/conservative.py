from typing import Dict, List
from .base import BasePublicationStrategy

class ConservativePublicationStrategy(BasePublicationStrategy):
    """
    Conservative publication strategy.
    - Default profile is public_minimal
    - Strict redaction
    - Low quarantine threshold
    """

    def get_default_profile(self) -> str:
        return "public_minimal"

    def allowed_profiles(self) -> List[str]:
        return ["public_minimal", "internal_publication_preview"]

    def evaluate_quarantine_threshold(self, malformed_intake_rate: float) -> bool:
        return malformed_intake_rate > 0.05
