import json
import logging
from typing import Dict, Any
from .contracts import (
    ArbitrationRailEvidenceRecord,
    RecoveryFabricPacketRecord,
    ProofMeshReplayRecord,
    VisibilityLedgerSuppressionRecord
)
from .arbitration_rails import build_continuity_arbitration_rail, summarize_continuity_arbitration_rail
from .recovery_fabrics import build_scheduler_recovery_fabric, summarize_scheduler_recovery_fabric
from .archive_proof_meshes import build_archive_proof_mesh, summarize_archive_proof_mesh
from .visibility_ledgers import build_worldwide_visibility_ledger, summarize_worldwide_visibility_ledger

logger = logging.getLogger(__name__)

def run_continuity_arbitration_hardening_pass() -> Dict[str, Any]:
    # 1. Arbitrary Evidence
    fresh_evidence = ArbitrationRailEvidenceRecord(evidence_id="e1", is_fresh=True, evidence_type="scheduler_proof")
    stale_evidence = ArbitrationRailEvidenceRecord(evidence_id="e2", is_fresh=False, evidence_type="stale_recovery_proof")

    rail_1 = build_continuity_arbitration_rail("scheduler_truth_arbitration_rail", [fresh_evidence])
    rail_2 = build_continuity_arbitration_rail("archive_proof_arbitration_rail", [fresh_evidence, stale_evidence])

    # 2. Recovery Fabric
    fresh_packet = RecoveryFabricPacketRecord(packet_id="p1", payload_hash="hash1", is_stale=False)
    stale_packet = RecoveryFabricPacketRecord(packet_id="p2", payload_hash="hash2", is_stale=True)

    fabric_1 = build_scheduler_recovery_fabric("planetary_scheduler_recovery_fabric", [fresh_packet])
    fabric_2 = build_scheduler_recovery_fabric("composite_scheduler_recovery_fabric", [fresh_packet, stale_packet])

    # 3. Proof Mesh
    success_replay = ProofMeshReplayRecord(replay_id="r1", replay_successful=True)
    failed_replay = ProofMeshReplayRecord(replay_id="r2", replay_successful=False)

    mesh_1 = build_archive_proof_mesh("archive_lineage_proof_mesh", [], [success_replay])
    mesh_2 = build_archive_proof_mesh("composite_archive_proof_mesh", [], [failed_replay])

    # 4. Visibility Ledger
    suppression = VisibilityLedgerSuppressionRecord(suppression_id="s1", reason="Network partition")

    ledger_1 = build_worldwide_visibility_ledger("scheduler_truth_visibility_ledger", [], [])
    ledger_2 = build_worldwide_visibility_ledger("no_safe_visibility_ledger", [], [suppression])

    report = {
        "continuity_arbitration_rails": [
            summarize_continuity_arbitration_rail(rail_1),
            summarize_continuity_arbitration_rail(rail_2)
        ],
        "scheduler_recovery_fabrics": [
            summarize_scheduler_recovery_fabric(fabric_1),
            summarize_scheduler_recovery_fabric(fabric_2)
        ],
        "archive_proof_meshes": [
            summarize_archive_proof_mesh(mesh_1),
            summarize_archive_proof_mesh(mesh_2)
        ],
        "worldwide_visibility_ledgers": [
            summarize_worldwide_visibility_ledger(ledger_1),
            summarize_worldwide_visibility_ledger(ledger_2)
        ]
    }

    with open("recovery_fabric_report.json", "w") as f:
        json.dump(report, f, indent=2)

    return report
