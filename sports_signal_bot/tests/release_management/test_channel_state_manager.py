import os
import shutil

from sports_signal_bot.release_management.state import ChannelStateManager


def test_channel_state_manager_basic():
    test_dir = "tests/test_data_release"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    manager = ChannelStateManager(data_dir=test_dir)
    state = manager.get_active_channel_state("football", "1x2")

    assert state.active_stable_chain_id is None

    manager.promote_channel_pointer("football", "1x2", "stable", "chain_v1")
    state2 = manager.get_active_channel_state("football", "1x2")

    assert state2.active_stable_chain_id == "chain_v1"

    manager.promote_channel_pointer("football", "1x2", "canary", "chain_v2")
    state3 = manager.get_active_channel_state("football", "1x2")

    assert state3.active_canary_chain_id == "chain_v2"
    assert state3.active_stable_chain_id == "chain_v1"

    manager.freeze_channel("football", "1x2", "Testing freeze")
    state4 = manager.get_active_channel_state("football", "1x2")
    assert state4.frozen_channel_flags.get("system") is True

    shutil.rmtree(test_dir)
