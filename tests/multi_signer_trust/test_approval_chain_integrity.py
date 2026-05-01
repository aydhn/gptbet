from datetime import datetime
from sports_signal_bot.multi_signer_trust.chains import append_approval_chain_link, verify_approval_chain_integrity
from sports_signal_bot.multi_signer_trust.contracts import ApprovalProofChainRecord, ApprovalChainSummaryRecord, ApprovalChainHashRecord

def test_approval_chain_integrity():
    chain = ApprovalProofChainRecord(
        chain_id="c1", links=[],
        summary=ApprovalChainSummaryRecord(chain_id="c1", status="started", start_time=datetime.utcnow(), end_time=None),
        hash_record=ApprovalChainHashRecord(chain_id="c1", root_hash="", head_hash="", link_count=0)
    )

    chain = append_approval_chain_link(chain, "sign", "user1", "hash1")
    chain = append_approval_chain_link(chain, "approve", "system", "hash2")

    assert verify_approval_chain_integrity(chain) == True
    assert len(chain.links) == 2
