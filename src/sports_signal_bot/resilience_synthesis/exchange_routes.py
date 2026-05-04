from .contracts import ReplayExchangeRoutingRecord

def route_replay_exchange_packet(packet_id: str, evidence_complete: bool, sovereignty_allows: bool) -> ReplayExchangeRoutingRecord:
    if not sovereignty_allows:
        return ReplayExchangeRoutingRecord(
            routing_id=f"route_{packet_id}",
            route_outcome="blocked_replay_route",
            selected_target_ref=None
        )
    if not evidence_complete:
        return ReplayExchangeRoutingRecord(
            routing_id=f"route_{packet_id}",
            route_outcome="routed_review_only_replay",
            selected_target_ref="review_target"
        )
    return ReplayExchangeRoutingRecord(
         routing_id=f"route_{packet_id}",
         route_outcome="routed_bounded_replay",
         selected_target_ref="bounded_target"
    )

def replay_replay_exchange(route: ReplayExchangeRoutingRecord) -> str:
    if route.route_outcome == "blocked_replay_route":
         return "blocked"
    return "success"
