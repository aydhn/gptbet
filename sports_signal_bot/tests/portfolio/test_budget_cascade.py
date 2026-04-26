import pytest
from sports_signal_bot.portfolio.contracts import PortfolioConfig, ExposureBudgetRecord
from sports_signal_bot.portfolio.budgets import BudgetCascadeResolver

def test_budget_cascade_resolver_initialization():
    config = PortfolioConfig(
        daily_risk_budget_fraction=0.15,
        max_bucket_risk_fraction=0.05,
        sport_budget_caps={"football": 0.10},
        market_budget_caps={"1x2": 0.05},
        action_class_budget_caps={"approved_candidate": 0.15}
    )
    resolver = BudgetCascadeResolver(config)
    budget = resolver.initialize_budget()

    assert budget.global_daily_limit == 0.15
    assert budget.time_bucket_limit == 0.05
    assert budget.sport_limits["football"] == 0.10
    assert budget.market_limits["1x2"] == 0.05

def test_budget_cascade_compute_available():
    config = PortfolioConfig()
    resolver = BudgetCascadeResolver(config)
    budget = resolver.initialize_budget()

    # Assume default config limits: daily=0.15, bucket=0.05, football=0.10, 1x2=0.05, approved=0.15
    available = resolver.compute_available_budget_stack(budget, "football", "1x2", "approved_candidate")
    assert available == 0.05 # Limited by bucket and market

    # Consume some
    resolver.consume_budget(budget, "football", "1x2", "approved_candidate", 0.03)

    available_now = resolver.compute_available_budget_stack(budget, "football", "1x2", "approved_candidate")
    # Remaining bucket=0.02, remaining market=0.02
    assert available_now == pytest.approx(0.02)
