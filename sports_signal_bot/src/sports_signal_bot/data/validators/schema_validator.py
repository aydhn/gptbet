from typing import Any, Dict, List, Tuple

from sports_signal_bot.data.contracts.manifests import ValidationIssueRecord
from sports_signal_bot.data.validators.base import BaseValidator


class RequiredFieldsValidator(BaseValidator):
    def __init__(self, required_fields: List[str]):
        self.required_fields = required_fields

    def validate(
        self, records: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[ValidationIssueRecord]]:
        valid_records = []
        issues = []

        for idx, record in enumerate(records):
            is_valid = True
            for field in self.required_fields:
                if field not in record or record[field] is None or record[field] == "":
                    is_valid = False
                    issues.append(
                        ValidationIssueRecord(
                            level="error",
                            field=field,
                            issue_type="missing_required_field",
                            message=f"Required field '{field}' is missing or empty.",
                            record_id=str(
                                record.get(
                                    "source_event_id", record.get("event_id", idx)
                                )
                            ),
                        )
                    )

            if is_valid:
                valid_records.append(record)

        return valid_records, issues


class UniqueEventValidator(BaseValidator):
    def __init__(self, id_field: str = "source_event_id"):
        self.id_field = id_field

    def validate(
        self, records: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[ValidationIssueRecord]]:
        valid_records = []
        issues = []
        seen_ids = set()

        for idx, record in enumerate(records):
            record_id = record.get(self.id_field)
            if not record_id:
                # Let required fields validator handle missing IDs
                valid_records.append(record)
                continue

            if record_id in seen_ids:
                issues.append(
                    ValidationIssueRecord(
                        level="error",
                        field=self.id_field,
                        issue_type="duplicate_event",
                        message=f"Duplicate event found for id '{record_id}'.",
                        record_id=str(record_id),
                    )
                )
            else:
                seen_ids.add(record_id)
                valid_records.append(record)

        return valid_records, issues


class HomeAwayValidator(BaseValidator):
    def validate(
        self, records: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[ValidationIssueRecord]]:
        valid_records = []
        issues = []

        for idx, record in enumerate(records):
            home = record.get("home_team")
            away = record.get("away_team")

            if home and away and home == away:
                issues.append(
                    ValidationIssueRecord(
                        level="error",
                        field="teams",
                        issue_type="invalid_matchup",
                        message=f"Home team and away team are identical: {home}.",
                        record_id=str(
                            record.get("source_event_id", record.get("event_id", idx))
                        ),
                    )
                )
            else:
                valid_records.append(record)

        return valid_records, issues
