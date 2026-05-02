import pytest
from src.sports_signal_bot.resilience_fabric.game_day import enter_simulation_mode, exit_simulation_mode

def test_simulation_mode_transitions():
    state = enter_simulation_mode("stale_source_storm")
    assert state == "simulation_active"

    state = exit_simulation_mode("system")
    assert state == "live"
