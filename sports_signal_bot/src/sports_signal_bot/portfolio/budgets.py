from typing import Dict, List
from sports_signal_bot.portfolio.contracts import PortfolioConfig, ExposureBudgetRecord

class BudgetCascadeResolver:
    def __init__(self, config: PortfolioConfig):
        self.config = config

    def initialize_budget(self) -> ExposureBudgetRecord:
        return ExposureBudgetRecord(
            global_daily_limit=self.config.daily_risk_budget_fraction,
            global_daily_used=0.0,
            global_daily_remaining=self.config.daily_risk_budget_fraction,

            time_bucket_limit=self.config.max_bucket_risk_fraction,
            time_bucket_used=0.0,
            time_bucket_remaining=self.config.max_bucket_risk_fraction,

            sport_limits=self.config.sport_budget_caps.copy(),
            sport_used={k: 0.0 for k in self.config.sport_budget_caps},
            sport_remaining=self.config.sport_budget_caps.copy(),

            market_limits=self.config.market_budget_caps.copy(),
            market_used={k: 0.0 for k in self.config.market_budget_caps},
            market_remaining=self.config.market_budget_caps.copy(),

            action_class_limits=self.config.action_class_budget_caps.copy(),
            action_class_used={k: 0.0 for k in self.config.action_class_budget_caps},
            action_class_remaining=self.config.action_class_budget_caps.copy(),

            reserve_budget=self.config.reserve_budget_fraction
        )

    def compute_available_budget_stack(self, budget: ExposureBudgetRecord, sport: str, market: str, action_class: str) -> float:
        limits = [
            budget.global_daily_remaining,
            budget.time_bucket_remaining,
            budget.sport_remaining.get(sport, float('inf')),
            budget.market_remaining.get(market, float('inf')),
            budget.action_class_remaining.get(action_class, float('inf'))
        ]
        return max(0.0, min(limits))

    def consume_budget(self, budget: ExposureBudgetRecord, sport: str, market: str, action_class: str, amount: float):
        budget.global_daily_used += amount
        budget.global_daily_remaining = max(0.0, budget.global_daily_limit - budget.global_daily_used)

        budget.time_bucket_used += amount
        budget.time_bucket_remaining = max(0.0, budget.time_bucket_limit - budget.time_bucket_used)

        if sport in budget.sport_used:
            budget.sport_used[sport] += amount
            budget.sport_remaining[sport] = max(0.0, budget.sport_limits[sport] - budget.sport_used[sport])

        if market in budget.market_used:
            budget.market_used[market] += amount
            budget.market_remaining[market] = max(0.0, budget.market_limits[market] - budget.market_used[market])

        if action_class in budget.action_class_used:
            budget.action_class_used[action_class] += amount
            budget.action_class_remaining[action_class] = max(0.0, budget.action_class_limits[action_class] - budget.action_class_used[action_class])

    def reset_bucket_budget(self, budget: ExposureBudgetRecord):
        budget.time_bucket_used = 0.0
        budget.time_bucket_remaining = budget.time_bucket_limit
