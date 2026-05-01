from .base import IntegrityStrategy
from ..contracts import SignedBundleRecord, DistributionPackageRecord

class BalancedIntegrityStrategy(IntegrityStrategy):
    def __init__(self):
        super().__init__("BalancedIntegrityStrategy")

    def evaluate_bundle(self, bundle: SignedBundleRecord) -> bool:
        return True

    def evaluate_import(self, package: DistributionPackageRecord) -> bool:
        return True
