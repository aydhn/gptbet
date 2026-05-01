from typing import Dict, Any, List
from .contracts import ChallengeSubmissionRecord

def triage_submission(submission: ChallengeSubmissionRecord) -> ChallengeSubmissionRecord:
    if submission.issue_type == "redaction_leak_claim":
        submission.status = "under_initial_review"
    elif submission.trust_class == "unknown":
        submission.status = "quarantined_pending_review"
        submission.quarantined = True
    else:
        submission.status = "accepted_for_triage"
    return submission
