import json
import uuid
from typing import Dict, Any

from .quorum_attestations import build_governance_quorum_attestation, summarize_quorum_attestation
from .backplanes import build_signal_routing_backplane, add_backplane_channel, summarize_backplane_health
from .baseline_meshes import build_baseline_federation_mesh, add_baseline_mesh_edge, summarize_baseline_mesh_health
from .disputes import open_sovereign_audit_dispute, run_dispute_mediation, summarize_dispute_state
from .contracts import DisputeCaseRecord

def run_sovereign_mediation_pass() -> Dict[str, Any]:
    # 1. Quorum Attestations
    attestation = build_governance_quorum_attestation(
        council_case_ref="cc_123",
        council_ref="council_alpha",
        decision_type="bounded_approval",
        evidence_refs=["ev_1", "ev_2"],
        caveat_refs=["cav_1"]
    )

    # 2. Backplanes
    backplane = build_signal_routing_backplane("governance_signal_backplane")
    channel = add_backplane_channel(backplane, "seg_in", "seg_out")

    # 3. Baseline Meshes
    mesh = build_baseline_federation_mesh("sovereign_baseline_mesh")
    edge = add_baseline_mesh_edge(mesh, "node_a", "node_b")

    # 4. Disputes
    dispute = open_sovereign_audit_dispute(
        family="currentness_dispute",
        source_ref="proj_1",
        conflicting_refs=["proj_2"]
    )

    case = DisputeCaseRecord(
        dispute_case_id="dc_1",
        dispute_ref=dispute.dispute_id,
        case_family="audit_replay_dispute",
        input_claim_refs=["claim_1"],
        input_evidence_refs=["ev_1"],
        replay_requirement="match",
        sovereignty_constraints="none",
        mediation_needed=True,
        case_status="open"
    )

    mediation_decision = run_dispute_mediation(dispute, case)
    dispute.dispute_status = "dispute_resolved_with_caveats" if mediation_decision == "accept_bounded_projection_with_caveats" else "dispute_blocked"

    # Summaries
    summary = {
        "quorum_attestations": summarize_quorum_attestation(attestation),
        "backplanes": summarize_backplane_health(backplane),
        "baseline_meshes": summarize_baseline_mesh_health(mesh),
        "disputes": summarize_dispute_state(dispute),
        "mediation_outcome": mediation_decision
    }

    with open("sovereign_mediation_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary
