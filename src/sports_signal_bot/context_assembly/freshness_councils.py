import uuid
from typing import List
from .contracts import ProofFreshnessCouncilRecord

def build_proof_freshness_council(family: str, policy_ref: str) -> ProofFreshnessCouncilRecord:
    council_id = f"council_{uuid.uuid4().hex[:8]}"
    return ProofFreshnessCouncilRecord(
        proof_freshness_council_id=council_id,
        council_family=family,
        governed_proof_refs=[],
        participant_refs=[],
        quorum_policy_ref=policy_ref,
        precedence_policy_ref="default_precedence",
        backlog_ref="backlog_main",
        health_status="healthy"
    )

def summarize_proof_freshness_council(council: ProofFreshnessCouncilRecord) -> str:
    status = council.health_status
    if council.warnings:
        status = "degraded"
    return f"Council {council.proof_freshness_council_id} is {status}"
