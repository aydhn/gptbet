from datetime import datetime
from typing import List, Optional

from .contracts import (
    QuorumAttestationExchangeRecord,
    QuorumExchangePacketRecord,
    BackplaneClusterRecord,
    BaselineMeshCouncilRecord,
    BaselineCouncilCaseRecord,
    SovereignGovernanceExceptionLedgerRecord,
    GovernanceExceptionRecord
)
from .quorum_exchanges import validate_quorum_exchange_packet
from .clusters import compute_cluster_backpressure, evaluate_cluster_orchestration
from .baseline_councils import open_baseline_council_case, resolve_baseline_council_case
from .exceptions import open_governance_exception, validate_exception_boundedness

# QUORUM EXCHANGE + CLUSTER FLOW
def build_quorum_exchange_cluster_pipeline(
    packet: QuorumExchangePacketRecord,
    cluster: BackplaneClusterRecord
) -> str:
    if not validate_quorum_exchange_packet(packet):
        return "blocked: invalid packet"

    pressure = compute_cluster_backpressure(cluster)
    decision = evaluate_cluster_orchestration(cluster)

    if pressure in ["high", "critical"] or decision == "shift_to_review_only_channels":
        return "exchanged_review_only"

    return "exchanged_bounded_governance"

def validate_cluster_entry_for_quorum_packet(packet: QuorumExchangePacketRecord, cluster: BackplaneClusterRecord) -> bool:
    return True

def summarize_quorum_cluster_flow(packet: QuorumExchangePacketRecord, cluster: BackplaneClusterRecord) -> dict:
    return {
        "packet_status": packet.warnings,
        "cluster_health": cluster.health_status
    }

# BASELINE COUNCIL + EXCEPTION FLOW
def build_baseline_council_exception_pipeline(
    case: BaselineCouncilCaseRecord,
    ledger: SovereignGovernanceExceptionLedgerRecord
) -> str:
    resolution = resolve_baseline_council_case(case)
    if resolution != "resolved":
        return "exception_required"
    return "resolved"

def connect_council_decision_to_exception_ledger(
    case: BaselineCouncilCaseRecord,
    ledger: SovereignGovernanceExceptionLedgerRecord,
    exception: GovernanceExceptionRecord
):
    if not validate_exception_boundedness(exception):
        return
    ledger.active_exception_refs.append(exception.exception_id)

def summarize_council_exception_flow(case: BaselineCouncilCaseRecord, ledger: SovereignGovernanceExceptionLedgerRecord) -> dict:
    return {
        "case_status": case.case_status,
        "ledger_active_exceptions": len(ledger.active_exception_refs)
    }

# DISPUTE MEDIATION + EXCEPTION INTEGRATION
def project_dispute_outcome_into_exceptions(
    dispute_ref: str,
    ledger: SovereignGovernanceExceptionLedgerRecord,
    resolution_status: str
) -> Optional[GovernanceExceptionRecord]:
    if resolution_status == "unresolved":
        return open_governance_exception(
            exception_family="temporary_review_visibility_exception",
            opened_reason=f"Unresolved dispute {dispute_ref}",
            affected_scope_ref="dispute_scope",
            validity_window=3600
        )
    return None

def resolve_or_expire_dispute_linked_exception(
    exception: GovernanceExceptionRecord,
    resolution_status: str
):
    if resolution_status == "resolved":
        exception.decision_status = "exception_expired"

def summarize_dispute_exception_interaction(exception: GovernanceExceptionRecord) -> dict:
    return {
        "exception_id": exception.exception_id,
        "status": exception.decision_status
    }

# CURRENTNESS / CAVEAT / SCOPE RULES
def enforce_phase85_currentness_caveat_scope_rules(packet: QuorumExchangePacketRecord) -> bool:
    if not packet.caveat_refs:
        return False
    return True

def cap_phase85_outputs_due_to_staleness(packet: QuorumExchangePacketRecord):
    packet.attested_decision_type = "review_only"

def explain_phase85_downgrade_or_block(reason: str) -> str:
    return f"Downgraded/Blocked due to: {reason}"

# SOVEREIGNTY RULES
def enforce_sovereignty_across_phase85(packet: QuorumExchangePacketRecord) -> bool:
    return True

def preserve_local_deny_in_exceptions(exception: GovernanceExceptionRecord):
    exception.preserved_block_refs.append("local_deny")

def explain_sovereignty_phase85_effects(effect: str) -> str:
    return f"Sovereignty effect: {effect}"
