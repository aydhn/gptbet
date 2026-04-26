from typing import List, Dict
from sports_signal_bot.sizing.contracts import SizingDecisionRecord
from sports_signal_bot.portfolio.contracts import PortfolioCandidateRecord, PortfolioAllocationRecord

def build_portfolio_candidates_from_sizing(
    sizing_decisions: List[SizingDecisionRecord],
    priority_tier_mapping: Dict[str, int] = None
) -> List[PortfolioCandidateRecord]:
    """
    Converts individual sizing decisions into portfolio candidates for batch allocation.
    """
    if priority_tier_mapping is None:
        priority_tier_mapping = {"approved_candidate": 2, "candidate": 1}

    candidates = []
    for d in sizing_decisions:
        # We need an event_datetime_utc, fallback to created_at if missing in sizing output
        event_time = d.created_at # Assuming sizing decision has created_at as fallback

        c = PortfolioCandidateRecord(
            event_id=d.event_id,
            event_datetime_utc=event_time,
            sport=d.sport,
            market_type=d.market_type,
            action_class=d.action_class,
            selected_side=d.selected_side,
            proposed_stake_fraction=d.final_stake_fraction,
            proposed_stake_units=d.final_stake_units,
            bankroll_before_window=d.bankroll_before,
            signal_score=0.0, # Placeholder if missing
            edge_estimate=d.edge_estimate,
            confidence=1.0,
            uncertainty=0.0,
            disagreement=0.0,
            data_quality_score=1.0,
            decimal_odds=d.decimal_odds,
            action_priority_tier=priority_tier_mapping.get(d.action_class, 1)
        )
        candidates.append(c)

    return candidates

def feed_allocated_stakes_to_bankroll_replay(allocations: List[PortfolioAllocationRecord]) -> List[dict]:
    """
    Format allocations for bankroll overlay ingestion.
    """
    return [
        {
            "event_id": a.event_id,
            "market_type": a.market_type,
            "allocated_stake_units": a.allocated_stake_units,
            "allocated_stake_fraction": a.allocated_stake_fraction,
            "allocation_status": a.allocation_status.value
        }
        for a in allocations
    ]

def reconcile_proposed_vs_allocated(candidates: List[PortfolioCandidateRecord], allocations: List[PortfolioAllocationRecord]) -> dict:
    """
    Matches candidates with final allocations to show exactly what changed.
    """
    c_map = {c.event_id: c for c in candidates}
    reconciliation = []

    for a in allocations:
        c = c_map.get(a.event_id)
        if c:
            reconciliation.append({
                "event_id": a.event_id,
                "proposed_fraction": c.proposed_stake_fraction,
                "allocated_fraction": a.allocated_stake_fraction,
                "reduced": a.allocated_stake_fraction < c.proposed_stake_fraction,
                "reason": a.allocation_status.value
            })

    return {"reconciliation": reconciliation}

def propagate_allocation_warnings(allocations: List[PortfolioAllocationRecord]) -> List[str]:
    """
    Extracts all warnings from allocations for diagnostic logging.
    """
    warnings = []
    for a in allocations:
        if a.warnings:
            warnings.append(f"{a.event_id}: {', '.join(a.warnings)}")
        if a.allocation_status.value != "fully_allocated":
             warnings.append(f"{a.event_id} status: {a.allocation_status.value}")
    return warnings
