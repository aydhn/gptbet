import json
import hashlib
from typing import Dict, Any
from datetime import datetime

def _json_serial(obj: Any) -> Any:
    """JSON serializer for objects not serializable by default json code."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def canonicalize_for_signing(payload: Dict[str, Any], exclude_fields: list[str] = None) -> bytes:
    """
    Deterministically canonicalizes a dictionary for signing.
    Sorts keys, ignores whitespace outside of strings, and formats timestamps.
    """
    if exclude_fields:
        payload = {k: v for k, v in payload.items() if k not in exclude_fields}

    # Use separaters=(',', ':') to eliminate whitespace
    json_str = json.dumps(
        payload,
        sort_keys=True,
        separators=(',', ':'),
        default=_json_serial
    )
    return json_str.encode('utf-8')

def compute_hash(payload: Dict[str, Any], exclude_fields: list[str] = None) -> str:
    """Computes a SHA-256 hash of the canonicalized payload."""
    canonical_bytes = canonicalize_for_signing(payload, exclude_fields)
    return hashlib.sha256(canonical_bytes).hexdigest()

def compute_bundle_hash(bundle_payload: Dict[str, Any]) -> str:
    """Compute hash for a bundle payload."""
    return compute_hash(bundle_payload)

def compute_manifest_hash(manifest_payload: Dict[str, Any]) -> str:
    """Compute hash for a manifest payload."""
    return compute_hash(manifest_payload)

def compute_decision_hash(decision_payload: Dict[str, Any]) -> str:
    """Compute hash for a decision proof input or output."""
    return compute_hash(decision_payload)

def validate_canonicalization_stability(payload: Dict[str, Any]) -> bool:
    """Validates that hashing a payload multiple times yields the same result."""
    hash1 = compute_hash(payload)
    hash2 = compute_hash(payload)
    return hash1 == hash2
