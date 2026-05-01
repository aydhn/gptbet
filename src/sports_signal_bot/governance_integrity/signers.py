from typing import Dict, Optional, List
from .contracts import SignerRecord, TrustLevel, SignerStatus

class LocalSignerProvider:
    """Provides local signers for development and testing."""
    def __init__(self):
        self.signers: Dict[str, SignerRecord] = {}

        # Add a default dev signer
        self.register_signer(SignerRecord(
            signer_id="local_dev_signer",
            signer_family="development",
            signer_name="Local Dev Mode Signer",
            trust_level=TrustLevel.DEV,
            active_status=SignerStatus.ACTIVE,
            key_ref_placeholder="dev_key_ref",
            signing_scope=["*"],
            review_required=True
        ))

    def register_signer(self, signer: SignerRecord) -> None:
        """Register a new signer."""
        self.signers[signer.signer_id] = signer

    def get_signer(self, signer_id: str) -> Optional[SignerRecord]:
        """Retrieve a signer by ID."""
        return self.signers.get(signer_id)

    def revoke_signer(self, signer_id: str) -> None:
        """Revoke a signer."""
        if signer_id in self.signers:
            signer = self.signers[signer_id]
            signer.active_status = SignerStatus.REVOKED
            signer.trust_level = TrustLevel.REVOKED

# Global registry for demonstration
_global_signer_provider = LocalSignerProvider()

def get_signer_provider() -> LocalSignerProvider:
    return _global_signer_provider
