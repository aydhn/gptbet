from typing import List, Dict, Any
from ..contracts import (
    PatternCandidateRecord,
    RuleSuggestionRecordV2,
    SuggestionBundleRecord
)

class BaseLearningStrategy:
    def process_candidates(self, candidates: List[PatternCandidateRecord]) -> SuggestionBundleRecord:
        raise NotImplementedError("Subclasses must implement process_candidates")
