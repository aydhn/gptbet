from sports_signal_bot.remediation_lanes.tokens import build_bounded_execution_token
from sports_signal_bot.remediation_lanes.contracts import BoundedExecutionTokenFamily
from datetime import datetime

def test_build_token():
    token = build_bounded_execution_token("t1", BoundedExecutionTokenFamily.rehearsal_execution_token, "l1", [], {}, "appr1", datetime.now(), datetime.now())
    assert token.token_family == BoundedExecutionTokenFamily.rehearsal_execution_token
