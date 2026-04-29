import pytest
from sports_signal_bot.schema_governance.compatibility import classify_breaking_change

def test_breaking_change_classification_base():
    changes = classify_breaking_change({}, {})
    assert len(changes) == 0
