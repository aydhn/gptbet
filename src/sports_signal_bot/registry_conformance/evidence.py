# evidence.py
from datetime import datetime, timezone
import uuid
from typing import Dict, Any


def create_evidence_bundle(bundle_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "evidence_id": bundle_id or f"ev_{uuid.uuid4().hex[:8]}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
        "is_verified": True,
    }
