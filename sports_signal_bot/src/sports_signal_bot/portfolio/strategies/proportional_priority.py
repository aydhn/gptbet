from typing import List
from sports_signal_bot.portfolio.contracts import (
    PortfolioCandidateRecord,
    PortfolioAllocationRecord,
    ExposureBucketRecord,
    ExposureBudgetRecord,
    AllocationStatus
)
from sports_signal_bot.portfolio.strategies.base import BaseAllocationStrategy
from sports_signal_bot.portfolio.priorities import compute_allocation_priority, rank_candidates_within_bucket
from sports_signal_bot.portfolio.concentration import compute_concentration_risk
from sports_signal_bot.portfolio.correlation import detect_related_market_candidates

class ProportionalPriorityAllocation(BaseAllocationStrategy):

    def allocate_bucket(self, bucket: ExposureBucketRecord, budget: ExposureBudgetRecord, current_allocations: List[PortfolioCandidateRecord]) -> List[PortfolioAllocationRecord]:
        results = []

        # 1. Filter out correlation risks
        valid_candidates = []
        for candidate in bucket.candidates:
            correlation_risks = detect_related_market_candidates(candidate, current_allocations, self.config)
            if correlation_risks and self.config.same_event_related_market_guard:
                results.append(PortfolioAllocationRecord(
                    event_id=candidate.event_id,
                    sport=candidate.sport,
                    market_type=candidate.market_type,
                    event_datetime_utc=candidate.event_datetime_utc,
                    time_bucket_id=bucket.bucket_id,
                    proposed_stake_units=candidate.proposed_stake_units,
                    proposed_stake_fraction=candidate.proposed_stake_fraction,
                    allocated_stake_units=0.0,
                    allocated_stake_fraction=0.0,
                    allocation_status=AllocationStatus.SKIPPED_BY_CORRELATION_GUARD,
                    allocation_policy_name=self.describe(),
                    risk_budget_before=budget.global_daily_remaining,
                    risk_budget_after=budget.global_daily_remaining,
                    priority_score=compute_allocation_priority(candidate, self.config),
                    warnings=[r.reason for r in correlation_risks],
                    run_id=self.run_id
                ))
            else:
                valid_candidates.append(candidate)

        if not valid_candidates:
            return results

        # 2. Compute Priority Scores
        ranked_candidates = rank_candidates_within_bucket(valid_candidates, self.config)
        total_priority = sum(compute_allocation_priority(c, self.config) for c in ranked_candidates)

        # 3. Available bucket budget (simplistic overall available)
        available_bucket_budget = budget.time_bucket_remaining

        for candidate in ranked_candidates:
            priority = compute_allocation_priority(candidate, self.config)
            proportion = priority / total_priority if total_priority > 0 else 0

            # Max we can give based on proportional distribution of bucket budget
            proportional_cap = available_bucket_budget * proportion

            conc_record = compute_concentration_risk(candidate, current_allocations, self.config)
            proposed_frac = candidate.proposed_stake_fraction * (1.0 - conc_record.overall_penalty)

            # Apply all cascades
            available_cascade = self.budget_resolver.compute_available_budget_stack(budget, candidate.sport, candidate.market_type, candidate.action_class)

            # Final allowed is the minimum of proposed, proportional cap, and available in cascade
            allocated_frac = min(proposed_frac, proportional_cap, available_cascade)

            status = AllocationStatus.FULLY_ALLOCATED
            if allocated_frac == 0:
                status = AllocationStatus.SKIPPED_BY_BUDGET
            elif allocated_frac < candidate.proposed_stake_fraction:
                status = AllocationStatus.PARTIALLY_ALLOCATED

            estimated_units = allocated_frac * candidate.bankroll_before_window
            if estimated_units > 0 and estimated_units < self.config.minimum_allocatable_stake_units:
                status = AllocationStatus.SKIPPED_BELOW_MIN_STAKE
                allocated_frac = 0.0
                estimated_units = 0.0

            budget_before = budget.global_daily_remaining
            if allocated_frac > 0:
                self.budget_resolver.consume_budget(budget, candidate.sport, candidate.market_type, candidate.action_class, allocated_frac)
                current_allocations.append(candidate)
            budget_after = budget.global_daily_remaining

            results.append(PortfolioAllocationRecord(
                event_id=candidate.event_id,
                sport=candidate.sport,
                market_type=candidate.market_type,
                event_datetime_utc=candidate.event_datetime_utc,
                time_bucket_id=bucket.bucket_id,
                proposed_stake_units=candidate.proposed_stake_units,
                proposed_stake_fraction=candidate.proposed_stake_fraction,
                allocated_stake_units=estimated_units,
                allocated_stake_fraction=allocated_frac,
                allocation_status=status,
                allocation_policy_name=self.describe(),
                risk_budget_before=budget_before,
                risk_budget_after=budget_after,
                priority_score=priority,
                run_id=self.run_id
            ))

        return results
