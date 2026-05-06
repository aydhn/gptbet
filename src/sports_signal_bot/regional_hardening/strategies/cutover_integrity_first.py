from .base import BaseRegionalHardeningStrategy

class CutoverIntegrityFirstStrategy(BaseRegionalHardeningStrategy):
    def apply(self, context):
        return context
