from datetime import datetime
import uuid
from typing import List, Optional
from .contracts import CopilotSessionRecord

class RemediationCopilotSessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, incident_ref: str, recommended_playbook_refs: List[str]) -> CopilotSessionRecord:
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        session = CopilotSessionRecord(
            session_id=session_id,
            incident_ref=incident_ref,
            recommended_playbook_refs=recommended_playbook_refs,
            current_stage="recommendation_generated",
            warnings=[]
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[CopilotSessionRecord]:
        return self.sessions.get(session_id)

    def update_session_stage(self, session_id: str, new_stage: str) -> CopilotSessionRecord:
        session = self.get_session(session_id)
        if session:
            session.current_stage = new_stage
        return session
