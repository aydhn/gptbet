from .base import BaseResilienceSynthesisStrategy

class ConservativeResilienceSynthesisStrategy(BaseResilienceSynthesisStrategy):
    def synthesize(self, context: dict) -> dict:
        # Implementation for Conservative strategy
        return {"band": "review_only_resilience", "notes": "Conservative caps applied."}
