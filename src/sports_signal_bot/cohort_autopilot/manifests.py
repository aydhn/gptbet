from datetime import datetime
from typing import List
from .contracts import AdoptionAutopilotManifest, AutopilotDecisionRecord

def create_autopilot_manifest(active_cohorts: int, decisions: List[AutopilotDecisionRecord]) -> AdoptionAutopilotManifest:
    return AdoptionAutopilotManifest(
        manifest_id=f"man_{int(datetime.utcnow().timestamp())}",
        active_cohorts=active_cohorts,
        decisions=decisions
    )
