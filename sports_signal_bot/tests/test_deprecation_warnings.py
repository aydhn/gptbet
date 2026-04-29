import pytest
from sports_signal_bot.schema_governance.deprecations import detect_deprecated_usage

class MockContract:
    deprecated_fields = ["old_field"]

def test_deprecation_warnings():
    payload = {"old_field": "val"}
    contract = MockContract()
    usages = detect_deprecated_usage(payload, contract)
    assert len(usages) == 1
    assert usages[0].field_name == "old_field"
