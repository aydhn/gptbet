import pytest
from sports_signal_bot.schema_governance.compatibility import check_forward_compatibility, CompatibilityResultStatus

def test_forward_compatibility_base():
    result = check_forward_compatibility({}, {})
    assert result.status == CompatibilityResultStatus.FULLY_COMPATIBLE
    assert result.is_compatible is True
