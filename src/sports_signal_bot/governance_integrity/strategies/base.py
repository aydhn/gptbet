from typing import Dict, Any, List
from ..contracts import SignedBundleRecord, DistributionPackageRecord

class IntegrityStrategy:
    def __init__(self, name: str):
        self.name = name

    def evaluate_bundle(self, bundle: SignedBundleRecord) -> bool:
        raise NotImplementedError

    def evaluate_import(self, package: DistributionPackageRecord) -> bool:
        raise NotImplementedError
