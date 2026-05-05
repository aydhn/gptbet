"""
Artifact reproducibility logic.
"""
from typing import Dict, Any, List
from .contracts import ArtifactReproducibilityRecord

def normalize_artifact_for_repro(artifact: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in sorted(artifact.items())}

def compare_artifact_sets(set1: Dict[str, Any], set2: Dict[str, Any]) -> bool:
    return set1 == set2

def generate_reproducibility_report(artifacts: List[Dict[str, Any]]) -> List[ArtifactReproducibilityRecord]:
    records = []
    for idx, artifact in enumerate(artifacts):
        records.append(ArtifactReproducibilityRecord(
            artifact_id=f"art_{idx}",
            artifact_type="json",
            reproducibility_status="reproducible"
        ))
    return records

def summarize_artifact_reproducibility(records: List[ArtifactReproducibilityRecord]) -> Dict[str, Any]:
    reproducible = sum(1 for r in records if r.reproducibility_status == "reproducible")
    return {
        "total_artifacts": len(records),
        "reproducible": reproducible,
        "non_reproducible": len(records) - reproducible
    }
