from sports_signal_bot.release_management.contracts import PromotionRequestRecord, RequestType
from sports_signal_bot.release_management.state import ChannelStateManager
from sports_signal_bot.release_management.rollback import RollbackPlanner, RollbackExecutor

def test_rollback_execution():
    manager = ChannelStateManager(data_dir="tests/test_data_rollback")

    # Setup history
    manager.promote_channel_pointer("football", "1x2", "stable", "chain_v1")
    manager.promote_channel_pointer("football", "1x2", "stable", "chain_v2")

    state = manager.get_active_channel_state("football", "1x2")
    assert state.active_stable_chain_id == "chain_v2"
    assert state.previous_stable_chain_id == "chain_v1"

    planner = RollbackPlanner(manager)
    plan = planner.create_rollback_plan("football", "1x2", "Reverting bad v2")

    assert plan is not None
    assert plan.target.chain_group_id == "chain_v1"
    assert plan.validation.target_valid is True

    executor = RollbackExecutor(manager)
    execution = executor.execute_rollback(plan)

    assert execution.status == "success"

    state_after = manager.get_active_channel_state("football", "1x2")
    assert state_after.active_stable_chain_id == "chain_v1"
