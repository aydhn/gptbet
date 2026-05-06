from .base import BaseRegionalHardeningStrategy

class LiveFireVisibilityFirstStrategy(BaseRegionalHardeningStrategy):
    def apply(self, context):
        return context
