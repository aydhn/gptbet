from .base import BaseGovernanceFabricStrategy

class SovereigntyDominantCouncilStrategy(BaseGovernanceFabricStrategy):
    def get_name(self) -> str:
        return "SovereigntyDominantCouncilStrategy"

    def apply(self, context: dict) -> dict:
        # High bias towards review-only and sovereignty blocks
        return context
