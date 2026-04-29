import pytest
from sports_signal_bot.schema_governance.validation import ContractValidator

class MockContractReq:
    required_fields = ["req1"]

def test_schema_validation_runner():
    validator = ContractValidator()
    contract = MockContractReq()

    res = validator.validate({"req1": "val"}, contract)
    assert res.is_valid is True

    res2 = validator.validate({"other": "val"}, contract)
    assert res2.is_valid is False
