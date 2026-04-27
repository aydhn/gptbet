from typing import Optional
from .contracts import DegradeStateRecord

class DegradeManager:
    def __init__(self):
        self.active_degrade: Optional[DegradeStateRecord] = None

    def activate_degrade(self, level: str, reason: str) -> DegradeStateRecord:
        record = DegradeStateRecord(
            degrade_level=level,
            reason=reason
        )
        self.active_degrade = record
        return record

    def release_degrade(self):
        if self.active_degrade:
            self.active_degrade.active = False
            self.active_degrade = None

    def get_current_degrade(self) -> Optional[DegradeStateRecord]:
        return self.active_degrade
