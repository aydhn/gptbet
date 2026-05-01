from sports_signal_bot.verifier_portal.intake_api import validate_challenge_api_submission
from sports_signal_bot.verifier_portal.contracts import ChallengeSubmissionRecord

def test_validate_challenge_api_submission():
    sub1 = ChallengeSubmissionRecord(submission_id="s1", issue_type="proof_reference_mismatch", details="valid details string")
    val1 = validate_challenge_api_submission(sub1)
    assert val1.valid

    sub2 = ChallengeSubmissionRecord(submission_id="s2", issue_type="invalid_type", details="valid details string")
    val2 = validate_challenge_api_submission(sub2)
    assert not val2.valid
