from typing import List, Optional
from .contracts import ChallengeRecord, ChallengeStatus, WitnessStatementRecord
import datetime

class ChallengeEngine:
    def issue_challenge(self, origin_witness_id: str, target_ref: str, asserted_issue: str, severity: str = "medium") -> ChallengeRecord:
        return ChallengeRecord(
            challenge_id=f"chal_{datetime.datetime.utcnow().timestamp()}",
            challenge_family="transparency_anomaly_challenge",
            target_ref=target_ref,
            origin_witness_id=origin_witness_id,
            asserted_issue=asserted_issue,
            expected_response_type="proof_supplied",
            severity=severity,
            deadline=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            current_status=ChallengeStatus.CHALLENGE_OPENED
        )

    def collect_challenge_response(self, challenge: ChallengeRecord, response_payload: str) -> ChallengeRecord:
        challenge.current_status = ChallengeStatus.RESPONSE_RECEIVED
        return challenge

    def close_or_escalate_challenge(self, challenge: ChallengeRecord, is_resolved: bool) -> ChallengeRecord:
        if is_resolved:
            challenge.current_status = ChallengeStatus.RESOLVED_CONFIRMED
        else:
            challenge.current_status = ChallengeStatus.UNRESOLVED_ESCALATED
        return challenge
