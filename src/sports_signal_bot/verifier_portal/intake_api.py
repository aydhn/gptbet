from typing import Dict, Any, List
import uuid
from .contracts import ChallengeSubmissionRecord, ChallengeSubmissionResponseRecord, ChallengeAPISchemaRecord, SubmissionValidationRecord

ALLOWED_ISSUE_TAXONOMY = [
    "proof_reference_mismatch",
    "disclosure_staleness_claim",
    "missing_publication_claim",
    "witness_consensus_disagreement_claim",
    "notarization_claim_issue",
    "challenge_process_issue",
    "redaction_leak_claim",
    "supersession_visibility_issue"
]

def validate_allowed_issue_taxonomy(issue_type: str) -> bool:
    return issue_type in ALLOWED_ISSUE_TAXONOMY

def validate_challenge_api_submission(submission: ChallengeSubmissionRecord) -> SubmissionValidationRecord:
    if not validate_allowed_issue_taxonomy(submission.issue_type):
        return SubmissionValidationRecord(valid=False)
    if len(submission.details) < 10 or len(submission.details) > 10000:
        return SubmissionValidationRecord(valid=False)
    return SubmissionValidationRecord(valid=True)

def sanitize_submission_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Basic sanitization
    sanitized = {}
    for k, v in payload.items():
        if isinstance(v, str):
            sanitized[k] = v.replace("<script>", "").replace("</script>", "")
        else:
            sanitized[k] = v
    return sanitized

def infer_submission_trust_class(submission: ChallengeSubmissionRecord) -> str:
    # Mock inference
    if "proof" in submission.details.lower():
        return "high_trust"
    return "unknown"

def build_submission_response(submission: ChallengeSubmissionRecord, status: str, message: str) -> ChallengeSubmissionResponseRecord:
    return ChallengeSubmissionResponseRecord(
        response_id=str(uuid.uuid4()),
        submission_id=submission.submission_id,
        status=status,
        message=message
    )

def summarize_api_submission(submission: ChallengeSubmissionRecord) -> Dict[str, Any]:
    return {
        "submission_id": submission.submission_id,
        "issue_type": submission.issue_type,
        "status": submission.status,
        "trust_class": submission.trust_class
    }

def cluster_duplicate_submissions(submissions: List[ChallengeSubmissionRecord]) -> List[List[ChallengeSubmissionRecord]]:
    # Mock clustering
    clusters = {}
    for sub in submissions:
        key = sub.issue_type
        if key not in clusters:
            clusters[key] = []
        clusters[key].append(sub)
    return list(clusters.values())

def rate_limit_submission(profile_id: str, recent_submissions_count: int) -> bool:
    # Mock rate limiting
    return recent_submissions_count < 10

def prioritize_submission_for_review(submission: ChallengeSubmissionRecord) -> int:
    # Priority score (higher is better)
    score = 0
    if submission.trust_class == "high_trust":
        score += 50
    if submission.issue_type == "redaction_leak_claim":
        score += 100
    return score

def explain_intake_governance_decision(submission: ChallengeSubmissionRecord, decision: str) -> str:
    return f"Submission {submission.submission_id} was {decision} because of policy rules."
