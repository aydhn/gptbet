import uuid
from typing import List
from sports_signal_bot.execution_coordination.contracts import ContentionRecord, ContentionFamily, ContentionSeverity

class ContentionDetector:
    def __init__(self):
        self.active_contentions: List[ContentionRecord] = []

    def detect_contentions(self, requested_lane_refs: List[str], shared_surfaces: List[str]) -> List[ContentionRecord]:
        new_contentions = []
        # Mock detection logic
        if len(requested_lane_refs) > 1 and "shared_db" in shared_surfaces:
            contention = ContentionRecord(
                contention_id=f"cnt_{uuid.uuid4().hex[:8]}",
                contention_family=ContentionFamily.SHARED_SOURCE_CONTENTION,
                involved_lane_refs=requested_lane_refs,
                shared_surface="shared_db",
                severity=ContentionSeverity.HIGH,
                current_resolution_state="unresolved"
            )
            new_contentions.append(contention)
            self.active_contentions.append(contention)

        return new_contentions

    def resolve_contention(self, contention_id: str, arbitration_ref: str):
        for c in self.active_contentions:
            if c.contention_id == contention_id:
                c.current_resolution_state = "resolved"
                c.arbitration_ref = arbitration_ref
