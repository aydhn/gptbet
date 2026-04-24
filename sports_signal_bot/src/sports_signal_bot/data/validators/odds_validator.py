from typing import List, Dict, Any, Tuple
from sports_signal_bot.data.validators.base import BaseValidator
from sports_signal_bot.data.contracts.manifests import ValidationIssueRecord

class OddsSanityValidator(BaseValidator):
    def validate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[ValidationIssueRecord]]:
        valid_records = []
        issues = []

        for idx, record in enumerate(records):
            try:
                odds = float(record.get("decimal_odds", 0.0))
            except (ValueError, TypeError):
                 odds = 0.0

            if odds <= 1.0:
                issues.append(
                     ValidationIssueRecord(
                        level="error",
                        field="decimal_odds",
                        issue_type="invalid_odds",
                        message=f"Odds must be > 1.0, got {odds}.",
                        record_id=str(record.get('source_event_id', record.get('event_id', idx)))
                    )
                )
            else:
                valid_records.append(record)

        return valid_records, issues
