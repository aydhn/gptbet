from datetime import datetime
from src.sports_signal_bot.public_verification_gateway.index import build_publication_index
from src.sports_signal_bot.public_verification_gateway.contracts import PublicPacketRecord

def test_publication_index():
    p = PublicPacketRecord(
        packet_id="p1",
        bundle_id="b1",
        metadata={"profile": "public_minimal", "family": "f1"},
        claimed_content={},
        independently_checkable=[],
        proof_refs=["proof1"],
        redaction_notice="notice",
        caveats=[],
        publication_time=datetime.utcnow()
    )
    idx = build_publication_index("idx1", [p])
    assert len(idx.entries) == 1
    assert idx.entries[0].bundle_id == "b1"
    assert idx.entries[0].proof_coverage_summary == "1 proofs attached"
