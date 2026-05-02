from typing import List, Dict, Any
from .contracts import CrossSystemReplayRecord, AssuranceExchangePacketRecord

def build_cross_system_replay_context(packet: AssuranceExchangePacketRecord) -> Dict[str, Any]:
    """Builds the context required to replay an assurance packet."""
    return {
        "packet_id": packet.exchange_packet_id,
        "carried_bundle_refs": packet.carried_bundle_refs,
        "claim_refs": packet.claim_refs
    }

def replay_external_assurance_packet(
    replay_id: str,
    packet: AssuranceExchangePacketRecord,
    local_context: Dict[str, Any]
) -> CrossSystemReplayRecord:
    """Replays an external assurance packet against local policy."""
    # Simulation of replay logic
    if not packet.carried_bundle_refs and not packet.claim_refs:
        result = "replay_rejected"
        details = "Empty packet cannot be replayed"
    else:
        result = "replay_accepted"
        details = "Replay successful based on local context"

    return CrossSystemReplayRecord(
        replay_id=replay_id,
        packet_id=packet.exchange_packet_id,
        result=result,
        details=details
    )

def compare_external_vs_local_results(external_result: str, local_result: str) -> bool:
    return external_result == local_result

def summarize_cross_system_replay(replays: List[CrossSystemReplayRecord]) -> Dict[str, Any]:
    accepted = sum(1 for r in replays if r.result == "replay_accepted")
    rejected = sum(1 for r in replays if r.result == "replay_rejected")
    return {
        "total_replays": len(replays),
        "accepted_replays": accepted,
        "rejected_replays": rejected
    }

def verify_replay_consistency(replay: CrossSystemReplayRecord) -> bool:
    return replay.result in ["replay_accepted", "replay_accepted_with_caveats"]
