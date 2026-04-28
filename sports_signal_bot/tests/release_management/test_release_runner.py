from sports_signal_bot.release_management.contracts import PromotionRequestRecord, RequestType
from sports_signal_bot.release_management.runner import ReleaseRunner

def test_release_runner_standard_flow():
    runner = ReleaseRunner(data_dir="tests/test_data_runner")

    req = PromotionRequestRecord(
        request_id="req1",
        request_type=RequestType.promote_candidate_to_stable_direct,
        sport="football",
        market_type="1x2",
        target_chain_group_id="chain_new",
        requested_by="tester",
        rationale="test direct"
    )

    # Conservative strategy should block direct promotion
    res = runner.process_request(req, "conservative_promotion")
    assert res is None

    # Placeholder direct strategy should allow it
    res2 = runner.process_request(req, "direct_promotion_placeholder")
    assert res2 is not None
    assert getattr(res2, 'decision', None) == "approved"

    state = runner.state_manager.get_active_channel_state("football", "1x2")
    assert state.active_stable_chain_id == "chain_new"
