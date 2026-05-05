from .base import BaseContextAssemblyStrategy
from ..bundles import OUTPUT_BLOCKED

class SovereigntyDominantContextStrategy(BaseContextAssemblyStrategy):
    """
    context bundles hızlı cap’lenir
    strong bounded görünüm çok daha dar kalır
    """
    def apply_context_rules(self, bundle):
        bundle.bundle_status = OUTPUT_BLOCKED
