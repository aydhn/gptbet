from .base import BaseGovernanceFabricStrategy

class ConsortiumStrictStrategy(BaseGovernanceFabricStrategy):
    def get_name(self) -> str:
        return "ConsortiumStrictStrategy"

    def apply(self, context: dict) -> dict:
        # Strict provenance and corroboration
        return context
