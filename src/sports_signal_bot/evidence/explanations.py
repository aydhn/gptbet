from typing import Dict, Any, List, Optional
from sports_signal_bot.evidence.contracts import (
    ExplanationPacketRecord, EvidenceBundleRecord, CounterfactualHintRecord
)

def explain_why_decision(bundle: EvidenceBundleRecord, summary: str) -> str:
    # A base summarizer
    reasons = [c.claim_text for c in bundle.claims if c.claim_status in ["supported", "weakly_supported"]]
    if reasons:
        return f"Decision based on: {'; '.join(reasons)}"
    return "Decision rationale unclear due to lacking supported claims."

def explain_why_not(bundle: EvidenceBundleRecord, blocking_claims: List[str]) -> str:
    if blocking_claims:
        return f"Not approved because: {', '.join(blocking_claims)}"
    return "No explicit blocking reasons found in evidence."

def explain_block_reason(bundle: EvidenceBundleRecord) -> str:
    blocks = [c.claim_text for c in bundle.claims if "block" in c.claim_type or c.claim_status == "contradicted"]
    if blocks:
        return f"Blocked by: {', '.join(blocks)}"
    return "Blocked due to unspecified policy."
