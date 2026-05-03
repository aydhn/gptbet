import pytest
from datetime import datetime
from sports_signal_bot.corridor_governance.contracts import TreatyLifecycleStateRecord
from sports_signal_bot.corridor_governance.treaty_lifecycle import evaluate_treaty_transition

def test_valid_transition():
    state = TreatyLifecycleStateRecord(
        treaty_ref="t1", lifecycle_state="treaty_active", effective_from=datetime.now(), warnings=[]
    )
    assert evaluate_treaty_transition(state, "treaty_renewal_due") == True
    assert evaluate_treaty_transition(state, "treaty_expired") == True

def test_invalid_transition():
    state = TreatyLifecycleStateRecord(
        treaty_ref="t1", lifecycle_state="treaty_expired", effective_from=datetime.now(), warnings=[]
    )
    # Can't go from expired to active directly
    assert evaluate_treaty_transition(state, "treaty_active") == False
