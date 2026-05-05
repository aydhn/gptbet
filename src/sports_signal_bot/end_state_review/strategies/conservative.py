from .base import BaseEndStateReviewStrategy
from ..contracts import EndStateReviewBand, EndStateReviewOutputRecord

class ConservativeEndStateReviewStrategy(BaseEndStateReviewStrategy):
    """
    default
    stale currentness, freshness gaps, unresolved residues and caveat losses ağır baskın
    federations, closure routes and exchanged outputs hızlı caveated/stale olur
    no-safe visibility en yüksek önemde
    """
    def evaluate_assurance_federation(self, *args, **kwargs):
        pass

    def evaluate_closure_mesh(self, *args, **kwargs):
        pass

    def evaluate_assurance_exchange(self, *args, **kwargs):
        pass

    def evaluate_end_state_review(self, *args, **kwargs):
        # In a conservative strategy, missing evidence or residues default to lower bands
        return EndStateReviewOutputRecord(
            output_id="conservative_out",
            band=EndStateReviewBand.bounded_end_state_with_caveats,
            caveats=["stale_assumed", "no_safe_preserved"]
        )
