from sports_signal_bot.witness_mesh.contracts import ChallengeStatus
from sports_signal_bot.witness_mesh.challenges import ChallengeEngine

def test_challenge_lifecycle():
    engine = ChallengeEngine()
    challenge = engine.issue_challenge("w1", "ref1", "issue")
    assert challenge.current_status == ChallengeStatus.CHALLENGE_OPENED

    challenge = engine.collect_challenge_response(challenge, "proof")
    assert challenge.current_status == ChallengeStatus.RESPONSE_RECEIVED

    challenge = engine.close_or_escalate_challenge(challenge, is_resolved=True)
    assert challenge.current_status == ChallengeStatus.RESOLVED_CONFIRMED
