from sports_signal_bot.multi_signer_trust.manifests import build_trust_manifest
from sports_signal_bot.multi_signer_trust.contracts import TrustMode

def test_manifest_building():
    man = build_trust_manifest()
    assert man.version == "1.0.0"
    assert man.mode == TrustMode.STRICT_ACTIVE
