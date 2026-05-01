import hashlib
from datetime import datetime
from typing import Dict, Any, List
from .contracts import (
    GossipSummaryRecord, GossipEnvelopeRecord, GossipVerificationRecord, GossipTopic, VerificationStatus
)

class GossipManager:
    def __init__(self):
        self._envelopes: List[GossipEnvelopeRecord] = []

    def build_gossip_envelope(self, topic: GossipTopic, source_plane: str, details: Dict[str, Any], signature: str) -> GossipEnvelopeRecord:
        details_str = str(details)
        summary_hash = hashlib.sha256(details_str.encode('utf-8')).hexdigest()

        summary = GossipSummaryRecord(
            summary_id=f"gsum_{datetime.utcnow().timestamp()}",
            topic=topic,
            summary_hash=summary_hash,
            details=details
        )

        envelope = GossipEnvelopeRecord(
            envelope_id=f"genv_{datetime.utcnow().timestamp()}",
            source_plane=source_plane,
            payload=summary,
            signature=signature
        )
        self._envelopes.append(envelope)
        return envelope

    def validate_gossip_payload(self, envelope: GossipEnvelopeRecord) -> GossipVerificationRecord:
        # Dummy signature verification
        is_valid = bool(envelope.signature)

        return GossipVerificationRecord(
            verification_id=f"ver_{datetime.utcnow().timestamp()}",
            envelope_id=envelope.envelope_id,
            status=VerificationStatus.VERIFIED if is_valid else VerificationStatus.FAILED
        )

    def ingest_gossip_signal(self, envelope: GossipEnvelopeRecord):
        # Trigger verification upon ingestion
        ver_record = self.validate_gossip_payload(envelope)
        if ver_record.status != VerificationStatus.VERIFIED:
            raise ValueError(f"Gossip payload verification failed for {envelope.envelope_id}")
        return True
