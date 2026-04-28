from sports_signal_bot.release_management.contracts import PromotionRequestRecord, RequestType
from sports_signal_bot.release_management.guards import check_quarantined_block, check_freeze_active
from sports_signal_bot.release_management.state import ChannelStateManager

def test_quarantined_block():
    manager = ChannelStateManager(data_dir="tests/test_data_release_guards")
    manager.mark_artifact_quarantined("football", "1x2", "bad_chain")

    req = PromotionRequestRecord(
        request_id="req1",
        request_type=RequestType.promote_candidate_to_canary,
        sport="football",
        market_type="1x2",
        target_chain_group_id="bad_chain",
        requested_by="tester",
        rationale="test"
    )

    guard = check_quarantined_block(req, manager)
    assert not guard.passed
    assert guard.severity == "critical"

def test_freeze_active():
    manager = ChannelStateManager(data_dir="tests/test_data_release_guards")
    manager.freeze_channel("football", "1x2", "test freeze")

    req = PromotionRequestRecord(
        request_id="req1",
        request_type=RequestType.promote_candidate_to_canary,
        sport="football",
        market_type="1x2",
        target_chain_group_id="good_chain",
        requested_by="tester",
        rationale="test"
    )

    state = manager.get_active_channel_state("football", "1x2")
    guard = check_freeze_active(req, state)
    assert not guard.passed
