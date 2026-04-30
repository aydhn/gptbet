from typing import List
from sports_signal_bot.evidence.contracts import EvidenceBundleRecord

def compute_bundle_confidence(bundle: EvidenceBundleRecord) -> str:
    if not bundle.claims:
        return "insufficient_evidence"

    # Simple logic based on lowest support strength or disputes
    has_disputed = any(c.support_strength == "disputed" for c in bundle.claims)
    if has_disputed:
        return "disputed"

    has_low = any(c.support_strength == "low" for c in bundle.claims)
    if has_low:
        return "low"

    has_medium = any(c.support_strength == "medium" for c in bundle.claims)
    if has_medium:
        return "medium"

    return "high"

def collect_bundle_caveats(bundle: EvidenceBundleRecord) -> List[str]:
    caveats = []
    for c in bundle.claims:
        for caveat in c.caveats:
            if caveat not in caveats:
                caveats.append(caveat)
    return caveats
