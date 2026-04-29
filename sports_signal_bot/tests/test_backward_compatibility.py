import pytest
from sports_signal_bot.schema_governance.compatibility import check_backward_compatibility, CompatibilityResultStatus

def test_backward_compatibility_base():
    result = check_backward_compatibility({}, {})
    assert result.status == CompatibilityResultStatus.FULLY_COMPATIBLE
    assert result.is_compatible is True
