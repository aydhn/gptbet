from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

def build_plane_council_packet(plane_id: str, local_issues: List[Any], budget_status: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "packet_id": f"pkt_{uuid.uuid4().hex[:8]}",
        "plane_id": plane_id,
        "issues": local_issues,
        "budget": budget_status,
        "timestamp": datetime.utcnow().isoformat()
    }

def aggregate_local_council(packets: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "council_id": f"ccl_{uuid.uuid4().hex[:8]}",
        "type": "local_aggregate",
        "packets_included": len(packets),
        "issues_found": sum(len(p.get("issues", [])) for p in packets)
    }

def aggregate_global_council(local_councils: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "global_council_id": f"gccl_{uuid.uuid4().hex[:8]}",
        "type": "global_aggregate",
        "councils_included": len(local_councils),
        "total_issues": sum(c.get("issues_found", 0) for c in local_councils)
    }

def summarize_federated_council_outcome(global_council: Dict[str, Any]) -> str:
    return f"Global Council {global_council['global_council_id']} evaluated {global_council['total_issues']} issues."
