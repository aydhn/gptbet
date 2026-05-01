from typing import Dict, Any, List
import uuid
from datetime import datetime

def explain_delegation_denied(plane_id: str, reason: str, precedence_notes: str) -> Dict[str, Any]:
    return {
        "evidence_id": f"evd_{uuid.uuid4().hex[:8]}",
        "type": "delegation_denial",
        "plane_id": plane_id,
        "reason": reason,
        "precedence_explanation": precedence_notes,
        "timestamp": datetime.utcnow().isoformat()
    }

def explain_escalation_triggered(source_plane: str, target_plane: str, conflict_details: str) -> Dict[str, Any]:
    return {
        "evidence_id": f"evd_{uuid.uuid4().hex[:8]}",
        "type": "escalation_triggered",
        "source": source_plane,
        "target": target_plane,
        "details": conflict_details,
        "timestamp": datetime.utcnow().isoformat()
    }

def explain_plane_suspended(plane_id: str, health_score: str, policy_refs: List[str]) -> Dict[str, Any]:
    return {
        "evidence_id": f"evd_{uuid.uuid4().hex[:8]}",
        "type": "plane_suspended",
        "plane_id": plane_id,
        "health": health_score,
        "policy_refs": policy_refs,
        "timestamp": datetime.utcnow().isoformat()
    }
