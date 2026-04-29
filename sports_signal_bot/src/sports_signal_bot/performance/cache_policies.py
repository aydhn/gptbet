from typing import Dict, Any

def resolve_cache_policy(policy_name: str) -> Dict[str, Any]:
    policies = {
        "no_cache": {"bypass": True, "write": False},
        "session_cache": {"bypass": False, "write": True, "ttl": 3600},
        "file_cache": {"bypass": False, "write": True, "ttl": 86400},
        "deterministic_artifact_cache": {"bypass": False, "write": True, "ttl": None},
        "time_bounded_cache": {"bypass": False, "write": True, "ttl": 7200},
        "dependency_hash_cache": {"bypass": False, "write": True, "ttl": None},
    }
    return policies.get(policy_name, policies["no_cache"])

def should_read_cache(policy: Dict[str, Any]) -> bool:
    return not policy.get("bypass", True)

def should_write_cache(policy: Dict[str, Any]) -> bool:
    return policy.get("write", False)

def should_bypass_cache(policy: Dict[str, Any]) -> bool:
    return policy.get("bypass", True)

def classify_cache_staleness(entry_time: float, current_time: float, ttl: int) -> bool:
    if ttl is None:
        return False
    return (current_time - entry_time) > ttl
