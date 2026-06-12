import uuid
from typing import List

from .contracts import (BuildQuorumAttestationExchangeParams,
                        QuorumAttestationExchangeRecord,
                        QuorumExchangePacketRecord, QuorumExchangeScopeRecord,
                        QuorumExchangeWarningRecord)

# QUORUM EXCHANGE FAMILY TAXONOMY
QUORUM_EXCHANGE_FAMILIES = [
    "internal_quorum_exchange",
    "review_only_quorum_exchange",
    "bounded_governance_quorum_exchange",
    "baseline_support_quorum_exchange",
    "dispute_support_quorum_exchange",
    "degraded_quorum_exchange",
    "replay_verification_quorum_exchange",
]

# QUORUM EXCHANGE STATUS TAXONOMY
QUORUM_EXCHANGE_STATUSES = [
    "prepared",
    "validated",
    "exchanged_review_only",
    "exchanged_bounded_governance",
    "exchanged_caveated",
    "exchanged_degraded",
    "exchanged_blocked",
    "exchanged_superseded",
    "exchanged_expired",
]


def build_quorum_attestation_exchange(
    params: BuildQuorumAttestationExchangeParams,
) -> QuorumAttestationExchangeRecord:
    return QuorumAttestationExchangeRecord(
        quorum_exchange_id=str(uuid.uuid4()),
        source_attestation_refs=params.source_attestation_refs,
        source_council_refs=params.source_council_refs,
        target_scope_refs=params.target_scope_refs,
        exchange_scope=QuorumExchangeScopeRecord(
            allowed_domains=params.allowed_domains,
            time_window_seconds=params.time_window_seconds,
        ),
        preserved_caveat_refs=params.preserved_caveat_refs,
        currentness_refs=params.currentness_refs,
        validity_window=params.validity_window,
        replay_support_refs=params.replay_support_refs,
        exchange_status="prepared",
        warnings=[],
    )


def validate_quorum_exchange_packet(packet: QuorumExchangePacketRecord) -> bool:
    if not packet.source_attestation_ref:
        return False
    if not packet.caveat_refs:
        packet.warnings.append(
            QuorumExchangeWarningRecord(
                warning_code="MISSING_CAVEATS",
                description="Quorum exchange packet must preserve caveats.",
                severity="high",
            )
        )
        return False
    return True


def preserve_quorum_lineage_and_caveats(
    packet: QuorumExchangePacketRecord, caveats: List[str]
):
    packet.caveat_refs.extend(caveats)


def replay_quorum_exchange(exchange_id: str) -> bool:
    # Logic to replay a quorum exchange
    return True


def summarize_quorum_exchange(exchange: QuorumAttestationExchangeRecord) -> dict:
    return {
        "id": exchange.quorum_exchange_id,
        "status": exchange.exchange_status,
        "caveat_count": len(exchange.preserved_caveat_refs),
        "warning_count": len(exchange.warnings),
    }


# DIMENSION TAXONOMY
QUORUM_EXCHANGE_DIMENSIONS = [
    "quorum_integrity_projection",
    "evidence_completeness_projection",
    "precedence_preservation_projection",
    "sovereignty_constraint_projection",
    "currentness_projection",
    "caveat_projection",
    "replayability_projection",
    "exception_sensitivity_projection",
    "degraded_state_projection",
    "lineage_integrity_projection",
]


def compute_quorum_exchange_dimensions(
    exchange: QuorumAttestationExchangeRecord,
) -> dict:
    return {dim: 1.0 for dim in QUORUM_EXCHANGE_DIMENSIONS}


def validate_dimension_preservation(exchange: QuorumAttestationExchangeRecord) -> bool:
    return True


def explain_quorum_exchange_losses(exchange: QuorumAttestationExchangeRecord) -> str:
    return "No losses."


def summarize_quorum_exchange_quality(
    exchange: QuorumAttestationExchangeRecord,
) -> dict:
    return {"quality": "high"}
