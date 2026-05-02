from typing import List, Dict, Any, Optional
from datetime import datetime
from .contracts import NotarizedPromotionEnvelopeRecord
from sports_signal_bot.assurance.contracts import ClaimValidityWindowRecord

def build_notarized_promotion_envelope(
    notarized_envelope_id: str,
    promotion_envelope_ref: str,
    digest_ref: str,
    notarization_ref: str,
    publication_scope: str,
    exchange_visibility_profile: str,
    valid_from: Optional[datetime] = None,
    valid_until: Optional[datetime] = None
) -> NotarizedPromotionEnvelopeRecord:
    """Builds a new notarized promotion envelope."""
    validity = ClaimValidityWindowRecord(
        valid_from=valid_from or datetime.utcnow(),
        valid_until=valid_until
    )
    return NotarizedPromotionEnvelopeRecord(
        notarized_envelope_id=notarized_envelope_id,
        promotion_envelope_ref=promotion_envelope_ref,
        digest_ref=digest_ref,
        notarization_ref=notarization_ref,
        publication_scope=publication_scope,
        exchange_visibility_profile=exchange_visibility_profile,
        validity_window=validity,
        verification_status="envelope_notarized",
        warnings=[]
    )

def verify_notarized_envelope(envelope: NotarizedPromotionEnvelopeRecord) -> bool:
    """Verifies a notarized envelope."""
    if not envelope.digest_ref or not envelope.notarization_ref:
        envelope.warnings.append("Missing digest or notarization ref")
        envelope.verification_status = "envelope_rejected"
        return False

    if envelope.validity_window.valid_until and envelope.validity_window.valid_until < datetime.utcnow():
        envelope.warnings.append("Notarized envelope is expired")
        envelope.verification_status = "envelope_quarantined"
        return False

    envelope.verification_status = "envelope_verified_local"
    return True

def attach_notarization_to_envelope(envelope_ref: str, notarization_ref: str) -> str:
    return f"attached_{notarization_ref}_to_{envelope_ref}"

def summarize_notarized_envelope_state(envelopes: List[NotarizedPromotionEnvelopeRecord]) -> Dict[str, Any]:
    verified = sum(1 for e in envelopes if e.verification_status == "envelope_verified_local")
    return {
        "total_envelopes": len(envelopes),
        "verified_envelopes": verified
    }
