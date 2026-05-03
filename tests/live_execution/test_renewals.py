from sports_signal_bot.live_execution.renewals import request_renewal, decide_renewal
from sports_signal_bot.live_execution.contracts import RenewalStatus

def test_renewal_workflow():
    ren = request_renewal("lane_1", "tok_old")
    assert ren.renewal_status == RenewalStatus.REQUESTED
    ren = decide_renewal(ren, approve=True, tighter_scope=True)
    assert ren.renewal_status == RenewalStatus.APPROVED_TIGHTER
    assert ren.new_token_ref == "token_new_tok_old"
