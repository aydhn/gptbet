import uuid
import datetime
from typing import List, Tuple
from sports_signal_bot.portfolio.contracts import (
    PortfolioCandidateRecord,
    PortfolioAllocationRecord,
    PortfolioRunManifest,
    PortfolioConfig,
    PortfolioSummaryRecord,
    ExposureBucketRecord
)
from sports_signal_bot.portfolio.factory import PortfolioStrategyFactory
from sports_signal_bot.portfolio.buckets import assign_time_buckets

class PortfolioRunner:
    def __init__(self, config: PortfolioConfig):
        self.config = config
        self.strategy = PortfolioStrategyFactory.create(config.default_allocation_strategy, config)
        self.run_id = str(uuid.uuid4())
        self.strategy.run_id = self.run_id

    def allocate(self, candidates: List[PortfolioCandidateRecord]) -> Tuple[List[PortfolioAllocationRecord], PortfolioRunManifest]:
        if not candidates:
            return [], self._empty_manifest()

        # 1. Bucket candidates
        buckets = assign_time_buckets(candidates, self.config.time_bucket_minutes)

        # 2. Initialize Budget
        budget = self.strategy.budget_resolver.initialize_budget()

        all_allocations = []
        current_allocations = []

        # 3. Process buckets chronologically
        for bucket in buckets:
            self.strategy.budget_resolver.reset_bucket_budget(budget)
            bucket_allocations = self.strategy.allocate_bucket(bucket, budget, current_allocations)
            all_allocations.extend(bucket_allocations)

        summary = self._generate_summary(all_allocations, budget)

        manifest = PortfolioRunManifest(
            run_id=self.run_id,
            config=self.config.dict(),
            summary=summary
        )

        return all_allocations, manifest

    def _generate_summary(self, allocations: List[PortfolioAllocationRecord], budget) -> PortfolioSummaryRecord:
        total = len(allocations)
        if total == 0:
            return PortfolioSummaryRecord()

        summary = PortfolioSummaryRecord(
            total_proposed_stake=sum(a.proposed_stake_fraction for a in allocations),
            total_allocated_stake=sum(a.allocated_stake_fraction for a in allocations),
            skipped_candidates=sum(1 for a in allocations if a.allocated_stake_fraction == 0),
            partially_allocated_candidates=sum(1 for a in allocations if 0 < a.allocated_stake_fraction < a.proposed_stake_fraction),
            concentration_penalty_counts=sum(1 for a in allocations if a.concentration_penalties),
            correlation_guard_skip_counts=sum(1 for a in allocations if "correlation" in a.allocation_status.value)
        )

        if summary.total_proposed_stake > 0:
            summary.allocation_ratio = summary.total_allocated_stake / summary.total_proposed_stake

        # Basic reductions avg
        reduced = [a for a in allocations if a.proposed_stake_fraction > 0 and a.allocated_stake_fraction < a.proposed_stake_fraction]
        if reduced:
            summary.average_reduction_pct = sum((a.proposed_stake_fraction - a.allocated_stake_fraction) / a.proposed_stake_fraction for a in reduced) / len(reduced)

        summary.daily_budget_utilization = budget.global_daily_used / budget.global_daily_limit if budget.global_daily_limit > 0 else 0

        return summary

    def _empty_manifest(self) -> PortfolioRunManifest:
        return PortfolioRunManifest(
            run_id=self.run_id,
            config=self.config.dict(),
            summary=PortfolioSummaryRecord()
        )
