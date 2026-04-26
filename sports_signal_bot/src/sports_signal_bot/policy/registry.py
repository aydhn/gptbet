from typing import Dict, Any, Type
from sports_signal_bot.policy.rules.base import BasePolicyRule
from sports_signal_bot.policy.rules.hard_blocks import HardBlockRuleSet
from sports_signal_bot.policy.rules.no_bet import NoBetRuleSet
from sports_signal_bot.policy.rules.candidate import CandidateRuleSet
from sports_signal_bot.policy.rules.approval import ApprovalRuleSet
from sports_signal_bot.policy.rules.watchlist import WatchlistRuleSet
from sports_signal_bot.policy.rules.regime_aware import RegimeRiskRule

class PolicyStrategyRegistry:
    _strategies: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str, setup: Dict[str, Any]):
        cls._strategies[name] = setup

    @classmethod
    def get(cls, name: str) -> Dict[str, Any]:
        return cls._strategies.get(name)

# Register default strategies
PolicyStrategyRegistry.register("balanced", {
    "hard_blocks": HardBlockRuleSet,
    "no_bet": NoBetRuleSet,
    "watchlist": WatchlistRuleSet,
    "candidate": CandidateRuleSet,
    "approval": ApprovalRuleSet,
    "extras": []
})

PolicyStrategyRegistry.register("conservative", {
    "hard_blocks": HardBlockRuleSet,
    "no_bet": NoBetRuleSet,
    "watchlist": WatchlistRuleSet,
    "candidate": CandidateRuleSet,
    "approval": ApprovalRuleSet,
    "extras": []
})

PolicyStrategyRegistry.register("aggressive_research", {
    "hard_blocks": HardBlockRuleSet,
    "no_bet": NoBetRuleSet, # Will be configured with wider bands
    "watchlist": WatchlistRuleSet,
    "candidate": CandidateRuleSet,
    "approval": ApprovalRuleSet,
    "extras": []
})

PolicyStrategyRegistry.register("regime_aware", {
    "hard_blocks": HardBlockRuleSet,
    "no_bet": NoBetRuleSet,
    "watchlist": WatchlistRuleSet,
    "candidate": CandidateRuleSet,
    "approval": ApprovalRuleSet,
    "extras": [RegimeRiskRule]
})
