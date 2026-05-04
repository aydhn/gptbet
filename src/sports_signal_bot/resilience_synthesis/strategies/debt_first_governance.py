from .base import BaseResilienceSynthesisStrategy

class DebtFirstGovernanceStrategy(BaseResilienceSynthesisStrategy):
    def synthesize(self, context: dict) -> dict:
        return {"band": "bounded_resilience_with_caveats", "notes": "Debt-first logic applied."}
