from typing import Optional
from .contracts import FreezeStateRecord

class FreezeManager:
    def __init__(self):
        self.active_freeze: Optional[FreezeStateRecord] = None

    def activate_freeze(self, reason: str, scope: str = "global") -> FreezeStateRecord:
        record = FreezeStateRecord(
            freeze_reason=reason,
            freeze_scope=scope,
            auto_release_policy="manual"
        )
        self.active_freeze = record
        return record

    def release_freeze(self):
        if self.active_freeze:
            self.active_freeze.active = False
            self.active_freeze = None

    def get_current_freeze(self) -> Optional[FreezeStateRecord]:
        return self.active_freeze
