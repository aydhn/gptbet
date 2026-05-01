from typing import Dict, List, Optional
from datetime import datetime
from .contracts import DisclosureBundleRecord

class DisclosureFamilyManager:
    def __init__(self):
        self.families = [
            "policy_bundle_disclosure",
            "transparency_checkpoint_disclosure",
            "decision_proof_disclosure",
            "witness_consensus_disclosure",
            "anomaly_summary_disclosure",
            "notarization_summary_disclosure",
            "external_exchange_summary_disclosure",
            "readiness_summary_disclosure",
            "governance_health_summary_disclosure"
        ]
        self.bundles: Dict[str, DisclosureBundleRecord] = {}

    def get_families(self) -> List[str]:
        return self.families

    def validate_family(self, family: str) -> bool:
        return family in self.families

    def register_bundle(self, bundle: DisclosureBundleRecord) -> None:
        if not self.validate_family(bundle.bundle_family):
            raise ValueError(f"Invalid disclosure family: {bundle.bundle_family}")
        self.bundles[bundle.disclosure_bundle_id] = bundle

    def get_bundle(self, bundle_id: str) -> Optional[DisclosureBundleRecord]:
        return self.bundles.get(bundle_id)
