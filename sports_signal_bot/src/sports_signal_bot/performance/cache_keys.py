import hashlib
import json
from typing import Dict, Any
from .contracts import CacheKeyRecord

def canonicalize_cache_inputs(inputs: Dict[str, Any]) -> str:
    return json.dumps(inputs, sort_keys=True)

def hash_cache_inputs(canonical_str: str) -> str:
    return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

def build_cache_key(inputs: Dict[str, Any]) -> CacheKeyRecord:
    canonical = canonicalize_cache_inputs(inputs)
    key = hash_cache_inputs(canonical)
    return CacheKeyRecord(key=key, inputs=inputs)

def explain_cache_key(record: CacheKeyRecord) -> str:
    return f"CacheKey({record.key}): {record.inputs}"
