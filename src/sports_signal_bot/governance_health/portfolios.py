import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    StabilizationProgramPortfolioRecord,
    PortfolioEntryRecord
)

def build_stabilization_program_portfolio(
    portfolio_family: str,
    priority_policy_ref: str,
    burden_policy_ref: str,
    dependency_policy_ref: str
) -> StabilizationProgramPortfolioRecord:
    return StabilizationProgramPortfolioRecord(
        portfolio_id=f"port_{uuid.uuid4().hex[:8]}",
        portfolio_family=portfolio_family,  # type: ignore
        priority_policy_ref=priority_policy_ref,
        burden_policy_ref=burden_policy_ref,
        dependency_policy_ref=dependency_policy_ref,
        health_status="initializing"
    )

def register_portfolio_entry(
    portfolio: StabilizationProgramPortfolioRecord,
    stabilization_program_ref: str,
    portfolio_role: str,
    current_stage_ref: str,
    priority_band: str
) -> PortfolioEntryRecord:
    entry = PortfolioEntryRecord(
        portfolio_entry_id=f"p_entry_{uuid.uuid4().hex[:8]}",
        stabilization_program_ref=stabilization_program_ref,
        portfolio_role=portfolio_role, # type: ignore
        current_stage_ref=current_stage_ref,
        priority_band=priority_band, # type: ignore
        portfolio_status="portfolio_balanced"
    )
    portfolio.entry_refs.append(entry.portfolio_entry_id)
    portfolio.monitored_program_refs.append(stabilization_program_ref)
    return entry

def compute_portfolio_burden(entries: List[PortfolioEntryRecord]) -> Dict[str, int]:
    burden_counts = {
        "replay_heavy": 0,
        "successor_blocked": 0,
        "exception_heavy": 0,
        "degraded": 0,
        "review_bias": 0,
        "blocked": 0
    }

    for entry in entries:
        if entry.portfolio_status == "portfolio_replay_heavy":
            burden_counts["replay_heavy"] += 1
        elif entry.portfolio_status == "portfolio_successor_blocked":
            burden_counts["successor_blocked"] += 1
        elif entry.portfolio_status == "portfolio_exception_heavy":
            burden_counts["exception_heavy"] += 1
        elif entry.portfolio_status == "portfolio_degraded":
            burden_counts["degraded"] += 1
        elif entry.portfolio_status == "portfolio_review_bias":
            burden_counts["review_bias"] += 1
        elif entry.portfolio_status == "portfolio_blocked":
            burden_counts["blocked"] += 1

    return burden_counts

def prioritize_portfolio_entries(entries: List[PortfolioEntryRecord]) -> List[PortfolioEntryRecord]:
    priority_order = {
        "stabilization_critical": 0,
        "successor_critical": 1,
        "replay_critical": 2,
        "burden_reduction_critical": 3,
        "review_only_support": 4,
        "regression_watch": 5,
        "opportunistic_cleanup": 6
    }

    return sorted(entries, key=lambda x: priority_order.get(x.priority_band, 99))

def summarize_portfolio_state(portfolio: StabilizationProgramPortfolioRecord, entries: List[PortfolioEntryRecord]) -> Dict[str, Any]:
    burdens = compute_portfolio_burden(entries)

    total_blocked = burdens["blocked"] + burdens["successor_blocked"]
    if total_blocked > 0:
        health = "blocked"
    elif burdens["degraded"] > 0 or burdens["exception_heavy"] > 0:
        health = "degraded"
    elif burdens["replay_heavy"] > 0:
        health = "backlogged"
    else:
        health = "balanced"

    portfolio.health_status = health

    return {
        "portfolio_id": portfolio.portfolio_id,
        "family": portfolio.portfolio_family,
        "entry_count": len(entries),
        "health_status": health,
        "burdens": burdens
    }
