from .base import BaseEndStateReviewStrategy
from ..contracts import EndStateReviewBand, EndStateReviewOutputRecord

class ClosureIntegrityFirstStrategy(BaseEndStateReviewStrategy):
    """
    closure integrity, freshness evidence ve trace applicability baskın
    weak evidence hızla review_only/no_safe olur
    closure and review caps daha görünür olur
    """
    def evaluate_assurance_federation(self, *args, **kwargs):
        pass

    def evaluate_closure_mesh(self, *args, **kwargs):
        pass

    def evaluate_assurance_exchange(self, *args, **kwargs):
        pass

    def evaluate_end_state_review(self, *args, **kwargs):
        return EndStateReviewOutputRecord(
            output_id="closure_out",
            band=EndStateReviewBand.review_only_end_state,
            caveats=["closure_caps_visible"]
        )
