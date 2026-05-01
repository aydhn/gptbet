from typing import List, Dict
from .contracts import PublicStyleReadinessRecord, ReadinessStatus, WitnessConsensusRecord, ChallengeRecord, TransparencyAnomalyRecord, ChallengeStatus
import datetime

class ReadinessScorer:
    def compute_public_style_readiness(self, consensus_records: List[WitnessConsensusRecord], challenges: List[ChallengeRecord], anomalies: List[TransparencyAnomalyRecord]) -> PublicStyleReadinessRecord:

        # Simplistic scoring
        open_challenges = len([c for c in challenges if c.current_status in [ChallengeStatus.CHALLENGE_OPENED, ChallengeStatus.AWAITING_RESPONSE, ChallengeStatus.UNRESOLVED_ESCALATED]])
        unresolved_anomalies = len(anomalies) # Assume all passed are unresolved for this mock

        score = 100
        blockers = []

        if open_challenges > 0:
            score -= 20
            blockers.append(f"{open_challenges} open challenges")

        if unresolved_anomalies > 0:
            score -= 30
            blockers.append(f"{unresolved_anomalies} unresolved anomalies")

        status = ReadinessStatus.NOT_READY
        if score > 90:
            status = ReadinessStatus.PUBLIC_STYLE_READINESS_CANDIDATE
        elif score > 70:
            status = ReadinessStatus.STRONG_INTERNAL_READINESS
        elif score > 50:
            status = ReadinessStatus.PARTIALLY_READY
        elif score > 30:
            status = ReadinessStatus.MINIMALLY_READY

        return PublicStyleReadinessRecord(
            readiness_id=f"readiness_{datetime.datetime.utcnow().timestamp()}",
            status=status,
            dimension_scores={"overall": score / 100.0},
            blockers=blockers,
            created_at=datetime.datetime.utcnow()
        )
