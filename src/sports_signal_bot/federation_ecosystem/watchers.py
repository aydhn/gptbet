from typing import Dict, Any, List

def run_registry_and_exchange_watchers(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    outcomes = []
    for event in events:
        if event.get("type") == "attestation_expired":
            outcomes.append({
                "action": "invalidate_exchange_path",
                "target": event.get("target_id")
            })
        elif event.get("type") == "sovereignty_suppression_increased":
            outcomes.append({
                "action": "downgrade_visibility",
                "target": event.get("target_id")
            })
        elif event.get("type") == "source_registry_pointer_changed":
            outcomes.append({
                "action": "require_review_reprojection",
                "target": event.get("target_id")
            })
    return outcomes

def invalidate_or_downgrade_federated_views(outcome: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    if outcome["action"] == "invalidate_exchange_path":
        state["status"] = "invalidated"
    elif outcome["action"] == "downgrade_visibility":
        state["visibility"] = "hidden_due_to_sovereignty"
    return state

def explain_watcher_outcome(outcome: Dict[str, Any]) -> str:
    return f"Watcher triggered {outcome['action']} on {outcome['target']}."

def summarize_watcher_activity(outcomes: List[Dict[str, Any]]) -> str:
    return f"Processed {len(outcomes)} watcher triggers."

def enforce_sovereignty_across_federation(participant_status: str, sovereignty_signal: str) -> str:
    if sovereignty_signal == "deny":
        return "hidden_due_to_sovereignty"
    return participant_status

def suppress_by_sovereignty_in_hub_and_registry(target_id: str) -> Dict[str, Any]:
    return {"id": target_id, "status": "suppressed_by_sovereignty"}

def explain_sovereignty_federation_effect(sovereignty_signal: str) -> str:
    if sovereignty_signal == "deny":
        return "Sovereignty deny overrides all ecosystem visibility."
    return "Sovereignty allows normal ecosystem visibility."
