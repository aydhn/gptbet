from typing import List, Dict, Any
from .contracts import RefreshAttempt, StateTransition, RefreshManifest

class RefreshHistoryStore:
    def __init__(self):
        self.attempts: List[RefreshAttempt] = []
        self.transitions: List[StateTransition] = []
        self.manifests: List[RefreshManifest] = []

    def record_attempt(self, attempt: RefreshAttempt):
        self.attempts.append(attempt)

    def record_transition(self, transition: StateTransition):
        self.transitions.append(transition)

    def record_manifest(self, manifest: RefreshManifest):
        self.manifests.append(manifest)

    def get_last_successful_attempt(self):
        for attempt in reversed(self.attempts):
            if attempt.status == "success" and attempt.validation_passed:
                return attempt
        return None

    def get_consecutive_failures(self) -> int:
        count = 0
        for attempt in reversed(self.attempts):
            if attempt.status == "failed" or not attempt.validation_passed:
                count += 1
            else:
                break
        return count
