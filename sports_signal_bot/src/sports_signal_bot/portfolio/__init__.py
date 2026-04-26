from sports_signal_bot.portfolio.contracts import (
    PortfolioCandidateRecord,
    PortfolioAllocationRecord,
    PortfolioConfig,
    PortfolioRunManifest
)
from sports_signal_bot.portfolio.runner import PortfolioRunner
from sports_signal_bot.portfolio.reporting import to_allocations_df, to_candidates_df
from sports_signal_bot.portfolio.cli.commands import portfolio_app

__all__ = [
    "PortfolioCandidateRecord",
    "PortfolioAllocationRecord",
    "PortfolioConfig",
    "PortfolioRunManifest",
    "PortfolioRunner",
    "to_allocations_df",
    "to_candidates_df",
    "portfolio_app",
]
from sports_signal_bot.portfolio.integration import (
    build_portfolio_candidates_from_sizing,
    feed_allocated_stakes_to_bankroll_replay,
    reconcile_proposed_vs_allocated,
    propagate_allocation_warnings
)
__all__.extend([
    "build_portfolio_candidates_from_sizing",
    "feed_allocated_stakes_to_bankroll_replay",
    "reconcile_proposed_vs_allocated",
    "propagate_allocation_warnings"
])
