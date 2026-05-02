from typing import Dict
from datetime import datetime
import uuid

def generate_assurance_manifest(summary: Dict) -> Dict:
    return {
        "manifest_id": f"assur_man_{uuid.uuid4().hex[:8]}",
        "created_at": datetime.utcnow().isoformat(),
        "summary": summary
    }
