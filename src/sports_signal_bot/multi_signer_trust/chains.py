from datetime import datetime
from typing import List, Optional, Tuple
import hashlib
from .contracts import (
    ThresholdDecisionRecord,
    ApprovalProofChainRecord,
    ApprovalChainLinkRecord,
    ApprovalChainSummaryRecord,
    ApprovalChainHashRecord
)

def build_multi_signer_decision_proof(
    target_ref: str,
    approval_ref: str,
    quorum_ref: str,
    attestation_refs: List[str],
    is_approved: bool,
    proof_chain_ref: str
) -> ThresholdDecisionRecord:
    return ThresholdDecisionRecord(
        decision_id=f"dec_{datetime.utcnow().timestamp()}",
        target_ref=target_ref,
        approval_ref=approval_ref,
        quorum_ref=quorum_ref,
        attestation_refs=attestation_refs,
        is_approved=is_approved,
        proof_chain_ref=proof_chain_ref,
        created_at=datetime.utcnow()
    )

def link_approval_chain_to_decision(
    decision: ThresholdDecisionRecord,
    ledger_ref: str
) -> ThresholdDecisionRecord:
    decision.ledger_ref = ledger_ref
    return decision

def verify_multi_signer_proof(decision: ThresholdDecisionRecord) -> bool:
    # Simplified verification
    return bool(decision.proof_chain_ref)

def summarize_decision_trust(decision: ThresholdDecisionRecord) -> str:
    status = "APPROVED" if decision.is_approved else "REJECTED"
    return f"Decision: {status} for {decision.target_ref} (Appr: {decision.approval_ref})"

def compute_link_hash(link: ApprovalChainLinkRecord) -> str:
    payload = f"{link.previous_link_id}:{link.action_type}:{link.actor}:{link.timestamp.isoformat()}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def append_approval_chain_link(
    chain: ApprovalProofChainRecord,
    action_type: str,
    actor: str,
    payload_hash: str
) -> ApprovalProofChainRecord:
    prev_id = chain.links[-1].link_id if chain.links else None

    new_link = ApprovalChainLinkRecord(
        link_id=f"link_{datetime.utcnow().timestamp()}",
        previous_link_id=prev_id,
        action_type=action_type,
        actor=actor,
        timestamp=datetime.utcnow(),
        payload_hash=payload_hash
    )

    link_hash = compute_link_hash(new_link)

    chain.links.append(new_link)
    chain.hash_record.head_hash = link_hash
    chain.hash_record.link_count = len(chain.links)

    if len(chain.links) == 1:
        chain.hash_record.root_hash = link_hash

    return chain

def detect_chain_gaps(chain: ApprovalProofChainRecord) -> List[str]:
    gaps = []
    for i in range(1, len(chain.links)):
        if chain.links[i].previous_link_id != chain.links[i-1].link_id:
            gaps.append(f"Gap between {chain.links[i-1].link_id} and {chain.links[i].link_id}")
    return gaps

def verify_approval_chain_integrity(chain: ApprovalProofChainRecord) -> bool:
    if not chain.links:
        return True

    if detect_chain_gaps(chain):
        return False

    return True

def export_approval_chain(chain: ApprovalProofChainRecord) -> dict:
    return chain.model_dump()
