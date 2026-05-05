from typing import Dict, Any, List

def summarize_alignment_federation_health(federations: List[Any]) -> Dict[str, Any]:
    healthy = sum(1 for f in federations if getattr(f, "health_status", None) == "healthy")
    degraded = sum(1 for f in federations if getattr(f, "health_status", None) == "degraded")
    critical = sum(1 for f in federations if getattr(f, "health_status", None) == "critical")
    return {"healthy": healthy, "degraded": degraded, "critical": critical, "total": len(federations)}

def summarize_tribunal_mesh_health(meshes: List[Any]) -> Dict[str, Any]:
    healthy = sum(1 for f in meshes if getattr(f, "health_status", None) == "healthy")
    degraded = sum(1 for f in meshes if getattr(f, "health_status", None) == "degraded")
    critical = sum(1 for f in meshes if getattr(f, "health_status", None) == "critical")
    return {"healthy": healthy, "degraded": degraded, "critical": critical, "total": len(meshes)}

def summarize_evidence_clearing(clearers: List[Any]) -> Dict[str, Any]:
    healthy = sum(1 for f in clearers if getattr(f, "health_status", None) == "healthy")
    degraded = sum(1 for f in clearers if getattr(f, "health_status", None) == "degraded")
    critical = sum(1 for f in clearers if getattr(f, "health_status", None) == "critical")
    return {"healthy": healthy, "degraded": degraded, "critical": critical, "total": len(clearers)}

def summarize_consistency_ledger(ledgers: List[Any]) -> Dict[str, Any]:
    healthy = sum(1 for f in ledgers if getattr(f, "health_status", None) == "healthy")
    degraded = sum(1 for f in ledgers if getattr(f, "health_status", None) == "degraded")
    critical = sum(1 for f in ledgers if getattr(f, "health_status", None) == "critical")
    return {"healthy": healthy, "degraded": degraded, "critical": critical, "total": len(ledgers)}
