from typing import Dict, Any, Optional
from pydantic import BaseModel
from .compatibility import CompatibilityResultRecord, CompatibilityResultStatus

class ContractValidationRecord(BaseModel):
    is_valid: bool
    errors: list[str] = []

class ContractValidator:
    def validate(self, payload: Dict[str, Any], contract_def) -> ContractValidationRecord:
        errors = []
        for req_field in contract_def.required_fields:
            if req_field not in payload:
                errors.append(f"Missing required field: {req_field}")

        return ContractValidationRecord(
            is_valid=len(errors) == 0,
            errors=errors
        )

class ManifestValidator:
    def validate(self, envelope, contract_def) -> ContractValidationRecord:
        return ContractValidationRecord(is_valid=True)

class PayloadValidator:
    def validate(self, payload, contract_def) -> ContractValidationRecord:
        return ContractValidationRecord(is_valid=True)

class VersionedValidationRunner:
    def run(self, payload, version) -> ContractValidationRecord:
        return ContractValidationRecord(is_valid=True)

class ValidationReporter:
    def report(self, validation_record: ContractValidationRecord) -> str:
        return "Valid" if validation_record.is_valid else f"Invalid: {', '.join(validation_record.errors)}"
