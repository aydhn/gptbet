from .contracts import CompilerFederationLinkRecord

def aggregate_federated_health_outputs(links: list[CompilerFederationLinkRecord]) -> str:
    # A simple mock aggregation strategy
    if any(link.link_status == "link_blocked" for link in links):
        return "aggregated_blocked"
    if any(link.link_status in ["link_caveated", "link_degraded"] for link in links):
         return "aggregated_bounded_health_with_caveats"
    return "aggregated_stabilized_with_caps"

def cap_federated_health_due_to_staleness(current_health: str, staleness: str) -> str:
    if staleness in ["stale", "expired"]:
         if current_health in ["aggregated_stabilized_with_caps", "aggregated_bounded_health_with_caveats"]:
             return "aggregated_review_only_health"
    return current_health

def preserve_no_safe_visibility_in_federation(current_health: str, has_no_safe_hint: bool) -> str:
    if has_no_safe_hint:
        return "aggregated_no_safe_preserved"
    return current_health

def explain_federated_health_output(health_status: str, reasons: list[str]) -> str:
    return f"Health Status: {health_status}. Reasons: {', '.join(reasons)}"
