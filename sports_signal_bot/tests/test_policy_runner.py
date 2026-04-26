import pytest

from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus
from sports_signal_bot.policy.runner import PolicyRunner
from sports_signal_bot.signal_scoring.contracts import (
    SignalPolicyInputRecord,
    SignalStatus,
)


@pytest.fixture
def base_config():
    return {
        "score_bands": {
            "rejected": 0.2,
            "no_bet": 0.4,
            "watchlist": 0.6,
            "candidate": 0.8,
        },
        "edge_bands": {"low": 0.01, "medium": 0.03, "high": 0.05},
        "uncertainty_limits": {"max_acceptable": 0.2},
        "disagreement_limits": {"max_acceptable": 0.3},
        "data_quality_limits": {"min_acceptable": 0.7},
        "approval_requirements": {
            "min_score": 0.8,
            "min_edge": 0.03,
            "max_uncertainty": 0.1,
            "max_disagreement": 0.2,
        },
        "no_bet_zone_rules": {
            "min_score": 0.4,
            "max_score": 0.6,
            "max_uncertainty": 0.3,
        },
        "hard_block_rules": {"min_score": 0.2, "min_data_quality": 0.5},
        "action_class_mapping": {
            "approved": "approved_candidate",
            "candidate": "candidate",
            "watchlist": "watchlist",
            "no_bet_zone": "no_action",
            "rejected": "blocked_candidate",
            "blocked": "blocked_candidate",
            "below_threshold": "watchlist",
            "weak_signal": "no_action",
        },
        "market_reference_required_for_approval": True,
        "regime_risk_penalties": {"high_risk": 0.1, "medium_risk": 0.05},
    }


def test_approved_signal(base_config):
    runner = PolicyRunner(base_config, "balanced")
    signal = SignalPolicyInputRecord(
        event_id="e1",
        sport="football",
        market_type="1x2",
        selection="home",
        final_probability=0.8,
        final_signal_score=0.9,
        edge_estimate=0.05,
        status=SignalStatus.SCORED,
        components_summary={
            "uncertainty_penalty": 0.05,
            "disagreement_penalty": 0.1,
            "data_quality_penalty": 0.0,
            "market_implied_probability": 0.75,
        },
    )
    decision = runner.evaluate_signal(signal)
    assert decision.signal_status == PolicySignalStatus.APPROVED
    assert decision.action_class == ActionClass.APPROVED_CANDIDATE


def test_hard_block_missing_ref(base_config):
    runner = PolicyRunner(base_config, "balanced")
    signal = SignalPolicyInputRecord(
        event_id="e1",
        sport="football",
        market_type="1x2",
        selection="home",
        final_probability=0.8,
        final_signal_score=0.9,
        edge_estimate=0.05,
        status=SignalStatus.SCORED,
        components_summary={
            "uncertainty_penalty": 0.05,
            "disagreement_penalty": 0.1,
            "data_quality_penalty": 0.0,
            # Missing market_implied_probability
        },
    )
    decision = runner.evaluate_signal(signal)
    assert decision.signal_status == PolicySignalStatus.BLOCKED
    assert "missing_market_reference" in decision.rationale_codes


def test_no_bet_zone_gray(base_config):
    runner = PolicyRunner(base_config, "balanced")
    signal = SignalPolicyInputRecord(
        event_id="e1",
        sport="football",
        market_type="1x2",
        selection="home",
        final_probability=0.5,
        final_signal_score=0.45,
        edge_estimate=0.02,
        status=SignalStatus.SCORED,
        components_summary={
            "market_implied_probability": 0.48,
            "data_quality_penalty": 0.0,
        },
    )
    decision = runner.evaluate_signal(signal)
    assert decision.signal_status == PolicySignalStatus.NO_BET_ZONE
    assert "no_bet_gray_zone" in decision.rationale_codes


def test_candidate_not_approved(base_config):
    runner = PolicyRunner(base_config, "balanced")
    signal = SignalPolicyInputRecord(
        event_id="e1",
        sport="football",
        market_type="1x2",
        selection="home",
        final_probability=0.7,
        final_signal_score=0.75,  # candidate > 0.6 but not approved < 0.8
        edge_estimate=0.04,
        status=SignalStatus.SCORED,
        components_summary={
            "uncertainty_penalty": 0.05,
            "disagreement_penalty": 0.1,
            "data_quality_penalty": 0.0,
            "market_implied_probability": 0.65,
        },
    )
    decision = runner.evaluate_signal(signal)
    assert decision.signal_status == PolicySignalStatus.CANDIDATE
    assert decision.action_class == ActionClass.CANDIDATE
