from typing import Dict, Any, List
from .contracts import FederatedRegistryRecord, AssuranceExchangePacketRecord, CrossSystemReplayRecord, ClaimTranslationRecord, AssuranceQuarantineRecord, NotarizedPromotionEnvelopeRecord

def build_assurance_exchange_summary(
    registries: List[FederatedRegistryRecord],
    packets: List[AssuranceExchangePacketRecord],
    translations: List[ClaimTranslationRecord],
    replays: List[CrossSystemReplayRecord],
    notarized_envelopes: List[NotarizedPromotionEnvelopeRecord],
    quarantines: List[AssuranceQuarantineRecord]
) -> Dict[str, Any]:
    """Builds a high-level KPI summary for the assurance exchange."""
    return {
        "federated_registry_count": len(registries),
        "exchange_packet_count": len(packets),
        "translation_safety_pass_rate": sum(1 for t in translations if t.semantic_loss_risk not in ["high", "critical"]) / len(translations) if translations else 1.0,
        "replay_acceptance_rate": sum(1 for r in replays if r.result == "replay_accepted") / len(replays) if replays else 1.0,
        "notarized_envelope_coverage": len(notarized_envelopes),
        "quarantine_count": len(quarantines),
        "quarantine_reasons_distribution": {} # Placeholder
    }
