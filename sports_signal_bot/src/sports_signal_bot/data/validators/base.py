from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from sports_signal_bot.data.contracts.manifests import ValidationIssueRecord

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[ValidationIssueRecord]]:
        """Returns a tuple of (valid_records, validation_issues)"""
        pass
