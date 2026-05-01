from sports_signal_bot.verifier_portal.intake_api import cluster_duplicate_submissions
from sports_signal_bot.verifier_portal.triage import triage_submission
from sports_signal_bot.verifier_portal.contracts import ChallengeSubmissionRecord

def test_cluster_duplicate_submissions():
    subs = [
        ChallengeSubmissionRecord(submission_id="s1", issue_type="t1", details="d1"),
        ChallengeSubmissionRecord(submission_id="s2", issue_type="t1", details="d2"),
        ChallengeSubmissionRecord(submission_id="s3", issue_type="t2", details="d3")
    ]
    clusters = cluster_duplicate_submissions(subs)
    assert len(clusters) == 2
    assert len(clusters[0]) == 2
    assert len(clusters[1]) == 1

def test_triage_submission():
    sub = ChallengeSubmissionRecord(submission_id="s1", issue_type="redaction_leak_claim", details="d1")
    sub = triage_submission(sub)
    assert sub.status == "under_initial_review"

    sub2 = ChallengeSubmissionRecord(submission_id="s2", issue_type="t1", details="d1", trust_class="unknown")
    sub2 = triage_submission(sub2)
    assert sub2.status == "quarantined_pending_review"
    assert sub2.quarantined
