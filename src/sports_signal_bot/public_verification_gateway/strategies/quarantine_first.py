from typing import Dict, List
from .base import BasePublicationStrategy

class QuarantineFirstPublicationStrategy(BasePublicationStrategy):
    """
    Quarantine-first publication strategy.
    - Heavily favors review over publication
    - Very strict threshold
    """

    def get_default_profile(self) -> str:
        return "review_quarantine_external"

    def allowed_profiles(self) -> List[str]:
        return ["public_minimal", "review_quarantine_external", "internal_publication_preview"]

    def evaluate_quarantine_threshold(self, malformed_intake_rate: float) -> bool:
        # Quarantine almost everything if there's any sign of issues
        return malformed_intake_rate > 0.01
