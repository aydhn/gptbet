class BaseGovernanceFabricStrategy:
    def get_name(self) -> str:
        return "BaseStrategy"

    def apply(self, context: dict) -> dict:
        return context
