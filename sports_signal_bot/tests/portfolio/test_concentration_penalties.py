import pytest
import datetime
from sports_signal_bot.portfolio.contracts import PortfolioConfig, PortfolioCandidateRecord
from sports_signal_bot.portfolio.concentration import compute_concentration_risk

def test_compute_concentration_risk():
    config = PortfolioConfig(
        concentration_penalty_weights={"sport": 0.1, "market": 0.1, "source": 0.05}
    )

    dt = datetime.datetime.now(datetime.timezone.utc)
    candidate = PortfolioCandidateRecord(
        event_id="E_NEW",
        event_datetime_utc=dt,
        sport="football",
        market_type="1x2",
        action_class="approved_candidate",
        selected_side="home",
        proposed_stake_fraction=0.02,
        proposed_stake_units=20.0,
        bankroll_before_window=1000.0,
        signal_score=0.8
    )

    current_allocations = [
        PortfolioCandidateRecord(
            event_id="E1",
            event_datetime_utc=dt,
            sport="football",
            market_type="1x2",
            action_class="approved_candidate",
            selected_side="home",
            proposed_stake_fraction=0.02,
            proposed_stake_units=20.0,
            bankroll_before_window=1000.0,
            signal_score=0.8
        ),
        PortfolioCandidateRecord(
            event_id="E2",
            event_datetime_utc=dt,
            sport="football",
            market_type="ou_2_5",
            action_class="approved_candidate",
            selected_side="over",
            proposed_stake_fraction=0.02,
            proposed_stake_units=20.0,
            bankroll_before_window=1000.0,
            signal_score=0.8
        )
    ]

    record = compute_concentration_risk(candidate, current_allocations, config)

    # Existing: 2 football, 1 1x2
    # penalty: sport (2 * 0.01 * 0.1) + market (1 * 0.01 * 0.1) = 0.002 + 0.001 = 0.003
    assert record.sport_concentration == pytest.approx(0.02)
    assert record.market_concentration == pytest.approx(0.01)
    assert record.overall_penalty == pytest.approx(0.003)
