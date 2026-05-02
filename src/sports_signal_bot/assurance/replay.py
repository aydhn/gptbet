from .contracts import ClaimReplayRecord
import uuid
from datetime import datetime

def replay_claim_verification(envelope_id: str) -> ClaimReplayRecord:
    return ClaimReplayRecord(
        replay_id=f"rep_{uuid.uuid4().hex[:8]}",
        original_envelope_id=envelope_id,
        replay_outcome="matched"
    )
