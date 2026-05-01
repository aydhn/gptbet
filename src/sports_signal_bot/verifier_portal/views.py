from typing import Dict, Any, List
from .contracts import PortalViewRecord

def get_available_views() -> List[PortalViewRecord]:
    return [
        PortalViewRecord(view_id="publication_index_view", view_name="Publication Index", description="Index of all publications"),
        PortalViewRecord(view_id="disclosure_bundle_view", view_name="Disclosure Bundle", description="Detailed disclosure bundles"),
        PortalViewRecord(view_id="checkpoint_summary_view", view_name="Checkpoint Summary", description="Summary of signed checkpoints"),
        PortalViewRecord(view_id="proof_summary_view", view_name="Proof Summary", description="Summary of proofs"),
        PortalViewRecord(view_id="decision_trace_view_publicsafe", view_name="Decision Trace", description="Public-safe decision traces"),
        PortalViewRecord(view_id="witness_consensus_view", view_name="Witness Consensus", description="Witness consensus view"),
        PortalViewRecord(view_id="anomaly_status_view", view_name="Anomaly Status", description="Status of anomalies"),
        PortalViewRecord(view_id="challenge_status_view", view_name="Challenge Status", description="Status of challenges"),
        PortalViewRecord(view_id="notarization_status_view", view_name="Notarization Status", description="Status of notarizations"),
        PortalViewRecord(view_id="readiness_dashboard_view", view_name="Readiness Dashboard", description="Readiness dashboard")
    ]
