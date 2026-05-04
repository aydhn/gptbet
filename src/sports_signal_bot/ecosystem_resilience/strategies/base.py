class BaseEcosystemResilienceStrategy:
    name = "base"

    def evaluate(self, context: dict) -> dict:
        return {"decision": "proceed"}
