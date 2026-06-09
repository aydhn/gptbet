import os
from typing import Any, Dict, List

from .contracts import (PortalQueryRecord, PortalResultRecord,
                        QuerySafetyDecisionRecord)
from .profiles import get_profile


def _has_forbidden_keys(data: Any) -> bool:
    if isinstance(data, dict):
        if "internal_path" in data or "key" in data:
            return True
        for val in data.values():
            if _has_forbidden_keys(val):
                return True
    elif isinstance(data, list):
        for item in data:
            if _has_forbidden_keys(item):
                return True
    return False


def validate_portal_query(query: PortalQueryRecord) -> QuerySafetyDecisionRecord:
    if "internal" in query.query_type.lower():
        return QuerySafetyDecisionRecord(
            safe=False, reason="Arbitrary raw internal queries are not allowed"
        )
    if _has_forbidden_keys(query.params):
        return QuerySafetyDecisionRecord(
            safe=False, reason="Sensitive internal path or key lookups are not allowed"
        )
    return QuerySafetyDecisionRecord(safe=True, reason="Query is safe")


def redact_query_results(results: Dict[str, Any], profile_id: str) -> Dict[str, Any]:
    profile = get_profile(profile_id)
    redacted = results.copy()
    if profile.signer_metadata_masking_level == "full":
        for item in redacted.get("items", []):
            if "signer_metadata" in item:
                item["signer_metadata"] = "[REDACTED]"
    elif profile.signer_metadata_masking_level == "partial":
        for item in redacted.get("items", []):
            if "signer_metadata" in item:
                item["signer_metadata"] = {
                    k: v
                    for k, v in item["signer_metadata"].items()
                    if k in ["signer_id", "timestamp"]
                }
    return redacted


def execute_profile_aware_query(query: PortalQueryRecord) -> PortalResultRecord:
    safety = validate_portal_query(query)
    if not safety.safe:
        raise ValueError(f"Unsafe query: {safety.reason}")

    # Mock data retrieval based on query type
    raw_data = {
        "status": "ok",
        "items": [
            {
                "id": 1,
                "data": "test",
                "signer_metadata": {
                    "key": os.getenv("MOCK_SIGNER_KEY", "mock_key_placeholder"),
                    "signer_id": "s1",
                    "timestamp": "now",
                },
            }
        ],
    }

    redacted_data = redact_query_results(raw_data, query.profile)

    return PortalResultRecord(
        result_id=f"res_{query.query_id}", query_id=query.query_id, data=redacted_data
    )


def attach_query_caveats(result: PortalResultRecord) -> PortalResultRecord:
    result.data["caveats"] = ["This is a read-only verification view."]
    return result


def summarize_query_response(result: PortalResultRecord) -> Dict[str, Any]:
    return {
        "result_id": result.result_id,
        "item_count": len(result.data.get("items", [])),
    }
