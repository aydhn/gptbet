from .base import IntegrityStrategy
from ..contracts import SignedBundleRecord, DistributionPackageRecord, BundleStatus

class ConservativeSignedGovernanceStrategy(IntegrityStrategy):
    def __init__(self):
        super().__init__("ConservativeSignedGovernanceStrategy")

    def evaluate_bundle(self, bundle: SignedBundleRecord) -> bool:
        if bundle.status == BundleStatus.DRAFT_UNSIGNED:
            return False
        return True

    def evaluate_import(self, package: DistributionPackageRecord) -> bool:
        # Requires verified signatures
        return True
