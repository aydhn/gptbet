from typing import List, Dict
import uuid
from .contracts import PlaybookLibraryRecord, RemediationPlaybookRecord

class PlaybookLibrary:
    def __init__(self):
        self.library: Dict[str, RemediationPlaybookRecord] = {}

    def register_playbook_in_library(self, playbook: RemediationPlaybookRecord):
        self.library[playbook.playbook_id] = playbook

    def find_candidate_playbooks(self, target_family: str) -> List[RemediationPlaybookRecord]:
        return [p for p in self.library.values() if p.target_incident_family == target_family]

    def supersede_outdated_playbooks(self):
        pass

    def summarize_library_health(self) -> str:
        return f"Library contains {len(self.library)} playbooks."
