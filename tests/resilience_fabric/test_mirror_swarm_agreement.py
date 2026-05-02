import pytest
from src.sports_signal_bot.resilience_fabric.contracts import MirrorSwarmRecord
from src.sports_signal_bot.resilience_fabric.swarms import evaluate_swarm_agreement, detect_split_brain_suspicion

def test_swarm_unanimous_agreement():
    swarm = MirrorSwarmRecord(
        swarm_id="swarm_1",
        swarm_family="registry_mirror_swarm",
        member_mirror_refs=["m1", "m2", "m3"],
        coverage_scope="all",
        agreement_policy="majority",
        lag_policy="strict",
        split_brain_policy="alert",
        health_status="healthy",
        warnings=[]
    )

    observations = {"m1": "state_A", "m2": "state_A", "m3": "state_A"}

    agreement = evaluate_swarm_agreement(swarm, observations, stale_members=[])
    assert agreement.agreement_result == "unanimous_agreement"
    assert detect_split_brain_suspicion(agreement) == "no_split_brain"

def test_swarm_split_observation():
    swarm = MirrorSwarmRecord(
        swarm_id="swarm_1",
        swarm_family="registry_mirror_swarm",
        member_mirror_refs=["m1", "m2", "m3"],
        coverage_scope="all",
        agreement_policy="majority",
        lag_policy="strict",
        split_brain_policy="alert",
        health_status="healthy",
        warnings=[]
    )

    observations = {"m1": "state_A", "m2": "state_A", "m3": "state_B"}

    agreement = evaluate_swarm_agreement(swarm, observations, stale_members=[])
    assert agreement.agreement_result == "split_observation"
    assert detect_split_brain_suspicion(agreement) == "suspected_split_brain"
