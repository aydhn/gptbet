from typing import List
from .contracts import ChallengeRoutingRecord, ChallengeTriageRecord, ChallengeExchangePacketRecord
import uuid

def compute_triage_priority(packet: ChallengeExchangePacketRecord) -> str:
    if packet.severity == "critical":
        return "high"
    elif packet.severity == "high":
        return "medium"
    return "low"

def incorporate_reputation_into_triage(triage: ChallengeTriageRecord, witness_reputation: float) -> ChallengeTriageRecord:
    if witness_reputation < 30:
        triage.assigned_responder_class = "internal_review"
    return triage

def detect_low_signal_challenge_spam(history: List[ChallengeExchangePacketRecord]) -> bool:
    return len(history) > 10

def explain_triage_decision(triage: ChallengeTriageRecord) -> str:
    return f"Triage {triage.triage_id} for {triage.challenge_ref} assigned priority {triage.priority} and class {triage.assigned_responder_class}"
