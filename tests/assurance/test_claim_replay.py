import pytest
from sports_signal_bot.assurance.replay import replay_claim_verification

def test_claim_replay():
    rec = replay_claim_verification("env_1")
    assert rec.replay_outcome == "matched"
