from sports_signal_bot.handoff.council import aggregate_council_lenses
from sports_signal_bot.handoff.contracts import CouncilVoteLikeRecord, CouncilDecisionType
import uuid

def test_aggregate_council_lenses_unanimous():
    votes = [
        CouncilVoteLikeRecord(vote_id=str(uuid.uuid4()), lens_name="l1", recommendation=CouncilDecisionType.APPROVE_HANDOFF),
        CouncilVoteLikeRecord(vote_id=str(uuid.uuid4()), lens_name="l2", recommendation=CouncilDecisionType.APPROVE_HANDOFF)
    ]
    assert aggregate_council_lenses(votes) == CouncilDecisionType.UNANIMOUS_APPROVE

def test_aggregate_council_lenses_reject():
    votes = [
        CouncilVoteLikeRecord(vote_id=str(uuid.uuid4()), lens_name="l1", recommendation=CouncilDecisionType.APPROVE_HANDOFF),
        CouncilVoteLikeRecord(vote_id=str(uuid.uuid4()), lens_name="l2", recommendation=CouncilDecisionType.REJECT_HANDOFF)
    ]
    assert aggregate_council_lenses(votes) == CouncilDecisionType.REJECT_HANDOFF
