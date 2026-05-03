from typing import Dict, List
from .contracts import (
    CorridorRegistryRecord,
    SovereignPolicyConformancePackRecord,
    AttestationExchangePacketRecord,
)


def inject_registry_and_pack_factors(
    base_scorecard: Dict,
    registry: CorridorRegistryRecord,
    pack: SovereignPolicyConformancePackRecord,
    exchange: AttestationExchangePacketRecord = None,
) -> Dict:

    scorecard = base_scorecard.copy()

    # 1) Registry health contribution
    health_score = 100
    if registry.health_status.status in ["stale_pressure", "caution"]:
        health_score -= 20
    elif registry.health_status.status in ["supersession_stressed", "degraded"]:
        health_score -= 50
    elif registry.health_status.status == "blocked":
        health_score = 0

    scorecard["registry_health_contribution"] = health_score

    # 2) Pack validity contribution
    pack_score = 100
    if pack.conformance_status == "conformant_with_caveats":
        pack_score -= 15
    elif pack.conformance_status in ["blocked_by_gap", "nonconformant", "expired"]:
        pack_score = 0

    scorecard["conformance_pack_contribution"] = pack_score

    # 3) Exchange caveats
    exchange_burden = 0
    if exchange:
        if exchange.exchange_status == "exchanged_caveated":
            exchange_burden = len(exchange.caveat_refs) * 10
        elif exchange.exchange_status in [
            "exchanged_blocked",
            "exchanged_expired",
            "exchanged_invalidated",
        ]:
            exchange_burden = 100

    scorecard["exchange_caveat_burden"] = exchange_burden

    # Final adjusted
    scorecard["adjusted_interoperability_score"] = min(
        100,
        max(
            0,
            (scorecard.get("base_score", 100) + health_score + pack_score) / 3
            - exchange_burden,
        ),
    )

    return scorecard


def explain_extended_scorecard(scorecard: Dict) -> str:
    return (
        f"Extended Scorecard -> "
        f"Base: {scorecard.get('base_score', 100)}, "
        f"Registry Health: {scorecard.get('registry_health_contribution', 0)}, "
        f"Pack Validity: {scorecard.get('conformance_pack_contribution', 0)}, "
        f"Exchange Burden: {scorecard.get('exchange_caveat_burden', 0)} "
        f"==> Adjusted: {scorecard.get('adjusted_interoperability_score', 0):.2f}"
    )


def summarize_scorecard_extension(scorecard: Dict) -> Dict:
    return {
        "adjusted_score": scorecard.get("adjusted_interoperability_score", 0),
        "factors": {
            "registry_health": scorecard.get("registry_health_contribution", 0),
            "pack_validity": scorecard.get("conformance_pack_contribution", 0),
            "exchange_burden": scorecard.get("exchange_caveat_burden", 0),
        },
    }
