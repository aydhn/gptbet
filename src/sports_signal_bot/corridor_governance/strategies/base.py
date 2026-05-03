class CorridorGovernanceStrategy:
    def get_strategy_name(self) -> str:
        raise NotImplementedError

    def evaluate_visibility(self) -> str:
        raise NotImplementedError
