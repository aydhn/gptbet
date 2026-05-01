from sports_signal_bot.multi_signer_trust.federated_verification import decide_federated_import_acceptance
from sports_signal_bot.multi_signer_trust.contracts import FederatedVerificationRecord, ImportLane

def test_federated_import_decision():
    ver = FederatedVerificationRecord(
        verification_id="v1", bundle_ref="b1", local_verified=True, remote_responses=[], final_lane=ImportLane.LOCAL_VERIFIED
    )

    dec1 = decide_federated_import_acceptance(ver, requires_federated=False)
    assert dec1.accepted == True

    dec2 = decide_federated_import_acceptance(ver, requires_federated=True)
    assert dec2.accepted == False
