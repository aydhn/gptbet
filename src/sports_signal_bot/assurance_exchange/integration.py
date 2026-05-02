from typing import Dict, Any, List
from .contracts import AssuranceExchangePacketRecord
from .packets import verify_exchange_packet_integrity
from .replay import build_cross_system_replay_context, replay_external_assurance_packet, verify_replay_consistency
from .translations import ClaimTranslationRecord, verify_translation_output

def run_interop_verification(
    packet: AssuranceExchangePacketRecord,
    translations: List[ClaimTranslationRecord]
) -> Dict[str, Any]:
    """Runs a full interoperability verification on an imported packet."""
    is_structurally_sound = verify_exchange_packet_integrity(packet)

    translation_safe = True
    for t in translations:
        if not verify_translation_output(t):
            translation_safe = False
            break

    context = build_cross_system_replay_context(packet)
    replay = replay_external_assurance_packet("test_replay", packet, context)
    replay_safe = verify_replay_consistency(replay)

    status = "verified" if (is_structurally_sound and translation_safe and replay_safe) else "quarantined"

    return {
        "packet_id": packet.exchange_packet_id,
        "structural_integrity": is_structurally_sound,
        "translation_safety": translation_safe,
        "replay_consistency": replay_safe,
        "final_status": status
    }

def build_interop_verification_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    verified = sum(1 for r in results if r["final_status"] == "verified")
    return {
        "total_verifications": len(results),
        "verified_count": verified,
        "quarantined_count": len(results) - verified
    }
