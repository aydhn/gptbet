from .base import BaseRegionalHardeningStrategy

class ConservativeRegionalHardeningStrategy(BaseRegionalHardeningStrategy):
    def apply(self, context):
        # strictest application
        return context
