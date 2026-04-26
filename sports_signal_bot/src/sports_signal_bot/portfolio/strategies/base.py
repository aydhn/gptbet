import abc
from typing import List
from sports_signal_bot.portfolio.contracts import (
    PortfolioCandidateRecord,
    PortfolioAllocationRecord,
    ExposureBucketRecord,
    ExposureBudgetRecord,
    PortfolioConfig
)
from sports_signal_bot.portfolio.budgets import BudgetCascadeResolver

class BaseAllocationStrategy(abc.ABC):
    def __init__(self, config: PortfolioConfig):
        self.config = config
        self.budget_resolver = BudgetCascadeResolver(config)
        self.run_id = ""

    @abc.abstractmethod
    def allocate_bucket(self, bucket: ExposureBucketRecord, budget: ExposureBudgetRecord, current_allocations: List[PortfolioCandidateRecord]) -> List[PortfolioAllocationRecord]:
        pass

    def describe(self) -> str:
        return self.__class__.__name__
