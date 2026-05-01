from datetime import datetime
from .contracts import TrustGovernanceManifest, TrustMode

def build_trust_manifest() -> TrustGovernanceManifest:
    return TrustGovernanceManifest(
        manifest_id=f"manifest_{datetime.utcnow().timestamp()}",
        version="1.0.0",
        active_policies=["default"],
        active_signers=5,
        recent_decisions=10,
        generated_at=datetime.utcnow(),
        mode=TrustMode.STRICT_ACTIVE
    )
