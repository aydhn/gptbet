from typing import List, Dict, Any
from .contracts import SourceEligibilityRecord, SourcePolicyDefinition
from .metadata import SourceMetadataRecord
from .policies import (BasicAvailabilityPolicy, QualityThresholdPolicy,
                       RegimeAwarePolicy, PreferredCalibratedPolicy, FallbackSafetyPolicy)

class SourcePolicyChain:
    def __init__(self, policy_definitions: List[SourcePolicyDefinition]):
        self.policies: List[Any] = []
        self._build_chain(policy_definitions)

    def _build_chain(self, definitions: List[SourcePolicyDefinition]):
        policy_map = {
            "BasicAvailabilityPolicy": BasicAvailabilityPolicy,
            "QualityThresholdPolicy": QualityThresholdPolicy,
            "RegimeAwarePolicy": RegimeAwarePolicy,
            "PreferredCalibratedPolicy": PreferredCalibratedPolicy,
            "FallbackSafetyPolicy": FallbackSafetyPolicy
        }

        for defn in definitions:
            if defn.policy_name in policy_map:
                self.policies.append(policy_map[defn.policy_name](defn))

    def run_chain(self,
                  metadata_map: Dict[str, SourceMetadataRecord],
                  eligibility_records: List[SourceEligibilityRecord],
                  context: Dict[str, Any]):

        context['metadata_map'] = metadata_map

        # Individual policies
        for r in eligibility_records:
            meta = metadata_map.get(r.source_name)
            if not meta: continue

            for policy in self.policies:
                if hasattr(policy, 'evaluate'):
                    policy.evaluate(meta, r, context)

        # Group policies
        for policy in self.policies:
            if hasattr(policy, 'evaluate_group'):
                policy.evaluate_group(eligibility_records, context)
