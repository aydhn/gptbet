from typing import Any, Dict

from sports_signal_bot.policy.registry import PolicyStrategyRegistry


class PolicyStrategyFactory:
    @staticmethod
    def build(strategy_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Builds a policy strategy mapping of rule sets based on the requested strategy."""

        # Override config based on strategy
        if strategy_name == "conservative":
            config = config.copy()
            reqs = config.get("approval_requirements", {})
            reqs["min_score"] = max(reqs.get("min_score", 0.8), 0.85)
            reqs["min_edge"] = max(reqs.get("min_edge", 0.03), 0.04)
            config["approval_requirements"] = reqs

            nb = config.get("no_bet_zone_rules", {})
            nb["max_score"] = max(nb.get("max_score", 0.6), 0.7)
            config["no_bet_zone_rules"] = nb

        elif strategy_name == "aggressive_research":
            config = config.copy()
            reqs = config.get("approval_requirements", {})
            reqs["min_score"] = min(reqs.get("min_score", 0.8), 0.75)
            config["approval_requirements"] = reqs

            nb = config.get("no_bet_zone_rules", {})
            nb["max_score"] = min(nb.get("max_score", 0.6), 0.5)
            config["no_bet_zone_rules"] = nb

        strategy_setup = PolicyStrategyRegistry.get(strategy_name)
        if not strategy_setup:
            strategy_setup = PolicyStrategyRegistry.get("balanced")

        built = {
            "name": strategy_name,
            "hard_blocks": strategy_setup["hard_blocks"](config),
            "no_bet": strategy_setup["no_bet"](config),
            "watchlist": strategy_setup["watchlist"](config),
            "candidate": strategy_setup["candidate"](config),
            "approval": strategy_setup["approval"](config),
            "extras": [cls(config) for cls in strategy_setup.get("extras", [])],
            "config": config,
        }
        return built
