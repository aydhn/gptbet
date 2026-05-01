from typing import List, Dict, Any
from .contracts import WitnessNodeRecord, WitnessMeshManifest, WitnessCoverageRecord, WitnessFamily, WitnessCapability
import datetime

class WitnessMeshBuilder:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def describe_witness_capabilities(self, witness: WitnessNodeRecord) -> List[str]:
        return [cap.value for cap in witness.verification_capabilities]

    def build_witness_mesh(self, nodes: List[WitnessNodeRecord]) -> WitnessMeshManifest:
        return WitnessMeshManifest(
            manifest_id=f"mesh_{datetime.datetime.utcnow().timestamp()}",
            nodes=nodes,
            created_at=datetime.datetime.utcnow()
        )

    def compute_witness_coverage(self, mesh: WitnessMeshManifest, target_refs: List[str]) -> List[WitnessCoverageRecord]:
        coverage = []
        for ref in target_refs:
            covering_nodes = []
            for node in mesh.nodes:
                # Simplistic simulation: assume if they share a common prefix they cover it
                if any(ref.startswith(fam) for fam in node.observed_log_families):
                    covering_nodes.append(node.witness_id)
            coverage.append(WitnessCoverageRecord(
                coverage_id=f"cov_{ref}",
                target_ref=ref,
                witness_ids=covering_nodes,
                covered=len(covering_nodes) > 0
            ))
        return coverage

    def detect_underwitnessed_scopes(self, coverage: List[WitnessCoverageRecord], min_witnesses: int = 2) -> List[WitnessCoverageRecord]:
        return [c for c in coverage if len(c.witness_ids) < min_witnesses]
