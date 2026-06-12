from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..contracts import (
    AdjudicationCaseRecord,
    AdjudicationDecisionRecord,
    FeedbackSignalRecord,
    ResolutionRecord,
)


class BaseAdjudicationStrategy(ABC):
    @abstractmethod
    def evaluate_case(self, case: AdjudicationCaseRecord) -> Dict[str, Any]:
        """Evaluate case characteristics before human review."""
        pass

    @abstractmethod
    def process_resolution(
        self, decision: AdjudicationDecisionRecord
    ) -> ResolutionRecord:
        """Process a human decision into a structured resolution."""
        pass

    @abstractmethod
    def determine_feedback_eligibility(
        self, resolution: ResolutionRecord
    ) -> Optional[FeedbackSignalRecord]:
        """Decide if this resolution should generate a feedback signal."""
        pass
