from typing import List
from .contracts import GateOutcome, PromotionEnvelopeRecord

def evaluate_assurance_gate(envelope: PromotionEnvelopeRecord) -> GateOutcome:
    if envelope.final_assurance_decision.value == "assurance_ready":
        return GateOutcome.pass_
    elif envelope.final_assurance_decision.value == "assurance_blocked":
        return GateOutcome.blocked
    return GateOutcome.review_required
