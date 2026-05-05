import pytest
from sports_signal_bot.concurrency_hardening.shared_state import register_shared_state_surface, register_state_owner

def test_register_shared_state_surface():
    surface = register_shared_state_surface("owner_1", "desc_1")
    assert surface.surface_desc == "desc_1"
    assert surface.status == "registered"

def test_register_state_owner():
    owner = register_state_owner("identity_1")
    assert owner.identity == "identity_1"
