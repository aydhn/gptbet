from .base import IntegrityStrategy
from ..contracts import SignedBundleRecord, DistributionPackageRecord

class ReviewFriendlyQuarantineStrategy(IntegrityStrategy):
    def __init__(self):
        super().__init__("ReviewFriendlyQuarantineStrategy")

    def evaluate_bundle(self, bundle: SignedBundleRecord) -> bool:
        return True

    def evaluate_import(self, package: DistributionPackageRecord) -> bool:
        # Puts things in quarantine by default
        return False
