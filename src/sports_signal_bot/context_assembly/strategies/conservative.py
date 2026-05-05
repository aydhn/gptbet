from .base import BaseContextAssemblyStrategy
from ..bundles import OUTPUT_BLOCKED, OUTPUT_CAVEATED

class ConservativeContextAssemblerStrategy(BaseContextAssemblyStrategy):
    """
    stale currentness, freshness gaps and caveat losses ağır baskın
    trace, exchange ve context bundles hızlı caveated/stale olur
    no-safe visibility en yüksek önemde
    """
    def apply_context_rules(self, bundle):
        if bundle.warnings:
            bundle.bundle_status = OUTPUT_BLOCKED
