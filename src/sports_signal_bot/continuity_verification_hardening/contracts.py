from enum import Enum
from typing import List, Optional, Dict
from dataclasses import dataclass, field, asdict

# --- Observatory Federation Models ---
class ObservatoryFederationFamily(str, Enum):
    bounded_observatory_federation = "bounded_observatory_federation"
    degraded_observatory_federation = "degraded_observatory_federation"
    archive_assisted_observatory_federation = "archive_assisted_observatory_federation"
    scheduler_visibility_observatory_federation = "scheduler_visibility_observatory_federation"
    no_safe_visibility_observatory_federation = "no_safe_visibility_observatory_federation"
    sovereignty_visibility_observatory_federation = "sovereignty_visibility_observatory_federation"
    composite_observatory_federation = "composite_observatory_federation"

class ObservatoryFederationStatus(str, Enum):
    federation_verified = "federation_verified"
    federation_caveated = "federation_caveated"
    federation_review_only = "federation_review_only"
    federation_gapped = "federation_gapped"
    federation_blocked = "federation_blocked"
    federation_overclaimed = "federation_overclaimed"

@dataclass
class FederatedObservatoryNodeRecord:
    node_id: str
    node_family: str
    owner_ref: str
    is_stale: bool = False

@dataclass
class ObservatoryFederationLinkRecord:
    link_id: str
    link_status: str
    lag_ms: int
    is_blocked: bool = False

@dataclass
class ObservatoryFederationAgreementRecord:
    agreement_id: str
    agreed_on: str

@dataclass
class ObservatoryFederationLagRecord:
    lag_id: str
    lag_ms: int

@dataclass
class ObservatoryFederationCaveatRecord:
    caveat_id: str
    description: str

@dataclass
class ObservatoryFederationContinuityRecord:
    continuity_id: str
    no_safe_visible: bool
    sovereignty_visible: bool

@dataclass
class ObservatoryFederationResidueRecord:
    residue_id: str
    unresolved_issues: int

@dataclass
class ObservatoryFederationWarningRecord:
    warning_id: str
    description: str

@dataclass
class ObservatoryFederationHealthRecord:
    health_id: str
    is_healthy: bool

@dataclass
class ObservatoryFederationManifestRecord:
    manifest_id: str
    created_at: str

@dataclass
class ObservatoryFederationRecord:
    observatory_federation_id: str
    federation_family: ObservatoryFederationFamily
    federation_status: ObservatoryFederationStatus
    member_observatory_refs: List[str] = field(default_factory=list)
    active_link_refs: List[str] = field(default_factory=list)
    agreement_refs: List[str] = field(default_factory=list)
    lag_refs: List[str] = field(default_factory=list)
    continuity_refs: List[str] = field(default_factory=list)
    residue_refs: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


    def dict(self):
        return asdict(self)

# --- Scheduler Proof Lane Models ---
class SchedulerProofLaneFamily(str, Enum):
    planetary_coverage_proof_lane = "planetary_coverage_proof_lane"
    archive_restore_proof_lane = "archive_restore_proof_lane"
    no_safe_visibility_proof_lane = "no_safe_visibility_proof_lane"
    sovereignty_visibility_proof_lane = "sovereignty_visibility_proof_lane"
    continuity_owner_proof_lane = "continuity_owner_proof_lane"
    executive_visibility_proof_lane = "executive_visibility_proof_lane"
    composite_scheduler_proof_lane = "composite_scheduler_proof_lane"

class SchedulerProofLaneStatus(str, Enum):
    lane_verified = "lane_verified"
    lane_caveated = "lane_caveated"
    lane_review_only = "lane_review_only"
    lane_gapped = "lane_gapped"
    lane_blocked = "lane_blocked"
    lane_overclaimed = "lane_overclaimed"

@dataclass
class SchedulerProofPacketRecord:
    packet_id: str
    is_stale: bool

@dataclass
class SchedulerProofEnvelopeRecord:
    envelope_id: str
    content: str

@dataclass
class SchedulerProofWindowRecord:
    window_id: str
    window_family: str

@dataclass
class SchedulerProofLineageRecord:
    lineage_id: str
    is_broken: bool

@dataclass
class SchedulerProofFreshnessRecord:
    freshness_id: str
    is_fresh: bool

@dataclass
class SchedulerProofLagRecord:
    lag_id: str
    lag_ms: int

@dataclass
class SchedulerProofResidueRecord:
    residue_id: str
    description: str

@dataclass
class SchedulerProofLaneWarningRecord:
    warning_id: str
    description: str

@dataclass
class SchedulerProofLaneHealthRecord:
    health_id: str
    is_healthy: bool

@dataclass
class SchedulerProofLaneManifestRecord:
    manifest_id: str
    created_at: str

@dataclass
class SchedulerProofLaneRecord:
    scheduler_proof_lane_id: str
    lane_family: SchedulerProofLaneFamily
    lane_status: SchedulerProofLaneStatus
    packet_refs: List[str] = field(default_factory=list)
    envelope_refs: List[str] = field(default_factory=list)
    window_refs: List[str] = field(default_factory=list)
    lineage_refs: List[str] = field(default_factory=list)
    freshness_refs: List[str] = field(default_factory=list)
    lag_refs: List[str] = field(default_factory=list)
    residue_refs: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def dict(self):
        return asdict(self)

# --- Audit Pulse Council Models ---
class AuditPulseCouncilFamily(str, Enum):
    follow_the_sun_pulse_council = "follow_the_sun_pulse_council"
    no_safe_visibility_pulse_council = "no_safe_visibility_pulse_council"
    sovereignty_visibility_pulse_council = "sovereignty_visibility_pulse_council"
    archive_restore_pulse_council = "archive_restore_pulse_council"
    continuity_owner_pulse_council = "continuity_owner_pulse_council"
    executive_visibility_pulse_council = "executive_visibility_pulse_council"
    composite_audit_pulse_council = "composite_audit_pulse_council"

class AuditPulseCouncilStatus(str, Enum):
    council_verified = "council_verified"
    council_caveated = "council_caveated"
    council_review_only = "council_review_only"
    council_gapped = "council_gapped"
    council_blocked = "council_blocked"
    council_overclaimed = "council_overclaimed"

@dataclass
class AuditPulseCouncilCaseRecord:
    case_id: str
    case_family: str

@dataclass
class AuditPulseCouncilEvidenceRecord:
    evidence_id: str
    is_sufficient: bool

@dataclass
class AuditPulseCouncilVoteRecord:
    vote_id: str
    vote: str

@dataclass
class AuditPulseCouncilDecisionRecord:
    decision_id: str
    decision_family: str

@dataclass
class AuditPulseCouncilCapRecord:
    cap_id: str
    description: str

@dataclass
class AuditPulseCouncilBacklogRecord:
    backlog_id: str

@dataclass
class AuditPulseCouncilResidueRecord:
    residue_id: str

@dataclass
class AuditPulseCouncilWarningRecord:
    warning_id: str

@dataclass
class AuditPulseCouncilHealthRecord:
    health_id: str

@dataclass
class AuditPulseCouncilManifestRecord:
    manifest_id: str

@dataclass
class AuditPulseCouncilRecord:
    audit_pulse_council_id: str
    council_family: AuditPulseCouncilFamily
    council_status: AuditPulseCouncilStatus
    case_refs: List[str] = field(default_factory=list)
    evidence_refs: List[str] = field(default_factory=list)
    vote_refs: List[str] = field(default_factory=list)
    decision_refs: List[str] = field(default_factory=list)
    cap_refs: List[str] = field(default_factory=list)
    residue_refs: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def dict(self):
        return asdict(self)

# --- Continuity Evidence Exchange Models ---
class ContinuityEvidenceExchangeFamily(str, Enum):
    scheduler_truth_evidence_exchange = "scheduler_truth_evidence_exchange"
    archive_lineage_evidence_exchange = "archive_lineage_evidence_exchange"
    no_safe_visibility_evidence_exchange = "no_safe_visibility_evidence_exchange"
    sovereignty_visibility_evidence_exchange = "sovereignty_visibility_evidence_exchange"
    continuity_owner_evidence_exchange = "continuity_owner_evidence_exchange"
    executive_visibility_evidence_exchange = "executive_visibility_evidence_exchange"
    composite_continuity_evidence_exchange = "composite_continuity_evidence_exchange"

class ContinuityEvidenceExchangeStatus(str, Enum):
    exchange_verified = "exchange_verified"
    exchange_caveated = "exchange_caveated"
    exchange_review_only = "exchange_review_only"
    exchange_gapped = "exchange_gapped"
    exchange_blocked = "exchange_blocked"
    exchange_overclaimed = "exchange_overclaimed"

@dataclass
class ContinuityEvidenceListingRecord:
    listing_id: str

@dataclass
class ContinuityEvidenceRequestRecord:
    request_id: str

@dataclass
class ContinuityEvidenceMatchRecord:
    match_id: str

@dataclass
class ContinuityEvidenceConstraintRecord:
    constraint_id: str

@dataclass
class ContinuityEvidenceTransferRecord:
    transfer_id: str

@dataclass
class ContinuityEvidenceResidueRecord:
    residue_id: str

@dataclass
class ContinuityEvidenceExchangeWarningRecord:
    warning_id: str

@dataclass
class ContinuityEvidenceExchangeHealthRecord:
    health_id: str

@dataclass
class ContinuityEvidenceExchangeManifestRecord:
    manifest_id: str

@dataclass
class ContinuityEvidenceExchangeRecord:
    continuity_evidence_exchange_id: str
    exchange_family: ContinuityEvidenceExchangeFamily
    exchange_status: ContinuityEvidenceExchangeStatus
    listing_refs: List[str] = field(default_factory=list)
    request_refs: List[str] = field(default_factory=list)
    match_refs: List[str] = field(default_factory=list)
    constraint_refs: List[str] = field(default_factory=list)
    transfer_refs: List[str] = field(default_factory=list)
    residue_refs: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def dict(self):
        return asdict(self)
