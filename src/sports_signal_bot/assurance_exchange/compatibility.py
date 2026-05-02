from typing import List, Dict, Any
from .contracts import CompatibilityMatrixRecord, CompatibilityDecisionRecord
from sports_signal_bot.assurance.contracts import ClaimFamily

def build_compatibility_matrix(matrix_id: str, name: str) -> CompatibilityMatrixRecord:
    """Builds a new compatibility matrix."""
    return CompatibilityMatrixRecord(
        matrix_id=matrix_id,
        name=name
    )

def evaluate_registry_compatibility(
    source_registry_profile: str,
    target_registry_profile: str,
    artifact_family: str
) -> str:
    """Evaluates compatibility between registries for an artifact."""
    if source_registry_profile == target_registry_profile:
        return "fully_interoperable"
    return "review_only_interoperable"

def detect_compatibility_gaps(source_profile: str, target_profile: str) -> List[str]:
    """Detects gaps in compatibility between two profiles."""
    gaps = []
    if source_profile != target_profile:
        gaps.append(f"Profile mismatch: {source_profile} vs {target_profile}")
    return gaps

def summarize_matrix_health(matrices: List[CompatibilityMatrixRecord]) -> Dict[str, Any]:
    return {
        "total_matrices": len(matrices)
    }
