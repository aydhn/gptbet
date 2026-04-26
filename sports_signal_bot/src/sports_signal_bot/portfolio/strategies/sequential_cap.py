from typing import List
import uuid
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

class SequentialCapAllocation(BaseAllocationStrategy):

    def allocate_bucket(self, bucket: ExposureBucketRecord, budget: ExposureBudgetRecord, current_allocations: List[PortfolioCandidateRecord]) -> List[PortfolioAllocationRecord]:
        results = []

        # Rank candidates
        ranked_candidates = rank_candidates_within_bucket(bucket.candidates, self.config)

        for candidate in ranked_candidates:
            warnings = []
            throttles = []
            penalties = []

            # 1. Correlation Guard
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
                continue

            # 2. Concentration Risk
            conc_record = compute_concentration_risk(candidate, current_allocations, self.config)
            proposed_frac = candidate.proposed_stake_fraction * (1.0 - conc_record.overall_penalty)

            if conc_record.overall_penalty > 0:
                penalties.append(f"Concentration penalty: {conc_record.overall_penalty:.2f}")

            # 3. Budget Cascade
            available = self.budget_resolver.compute_available_budget_stack(budget, candidate.sport, candidate.market_type, candidate.action_class)

            allocated_frac = min(proposed_frac, available)

            status = AllocationStatus.FULLY_ALLOCATED
            if allocated_frac == 0:
                status = AllocationStatus.SKIPPED_BY_BUDGET
            elif allocated_frac < candidate.proposed_stake_fraction:
                if conc_record.overall_penalty > 0 and allocated_frac == proposed_frac:
                    status = AllocationStatus.REDUCED_BY_CONCENTRATION
                else:
                    status = AllocationStatus.REDUCED_BY_BUDGET
            elif allocated_frac < candidate.proposed_stake_fraction and not self.config.partial_allocation_allowed:
                status = AllocationStatus.SKIPPED_BY_BUDGET
                allocated_frac = 0.0

            # Minimum stake check (assuming units = fraction * bankroll)
            # Roughly estimating units
            estimated_units = allocated_frac * candidate.bankroll_before_window
            if estimated_units > 0 and estimated_units < self.config.minimum_allocatable_stake_units:
                status = AllocationStatus.SKIPPED_BELOW_MIN_STAKE
                allocated_frac = 0.0
                estimated_units = 0.0

            budget_before = budget.global_daily_remaining

            if allocated_frac > 0:
                self.budget_resolver.consume_budget(budget, candidate.sport, candidate.market_type, candidate.action_class, allocated_frac)
                current_allocations.append(candidate) # Add to current allocations for next iterations

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
                concentration_penalties=penalties,
                throttle_reasons=throttles,
                priority_score=compute_allocation_priority(candidate, self.config),
                warnings=warnings,
                run_id=self.run_id
            ))

        return results
