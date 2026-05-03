from typing import List
import uuid
from datetime import datetime, timezone
from .contracts import ResilienceAdvisorManifest, ResilienceAdvisorRecord

def generate_resilience_advisor_manifest(advisors: List[ResilienceAdvisorRecord]) -> ResilienceAdvisorManifest:
    return ResilienceAdvisorManifest(
        manifest_id=f"manifest_{uuid.uuid4().hex[:8]}",
        advisors=advisors,
        timestamp=datetime.now(timezone.utc)
    )
