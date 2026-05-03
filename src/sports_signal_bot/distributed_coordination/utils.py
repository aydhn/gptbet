import hashlib
from typing import Dict, Any

def generate_deterministic_cluster_hash(state_dict: Dict[str, Any]) -> str:
    """Generates a deterministic hash from a state dictionary for cluster fingerprinting."""
    canonical_string = str(sorted(state_dict.items()))
    return hashlib.sha256(canonical_string.encode('utf-8')).hexdigest()
