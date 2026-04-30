from typing import Dict, Any, List
from .contracts import AdoptionSummaryRecord, StableAdoptionRecord

class StableAdoptionReportingHooks:
    @staticmethod
    def calculate_activation_approval_yield(adoptions: List[StableAdoptionRecord]) -> float:
        if not adoptions:
            return 0.0
        approved = sum(1 for a in adoptions if a.current_status in ["stable_pointer_advanced", "post_activation_verified", "adoption_completed"])
        return approved / len(adoptions)

    @staticmethod
    def calculate_post_activation_clean_rate(adoptions: List[StableAdoptionRecord]) -> float:
        verified = [a for a in adoptions if a.current_status in ["post_activation_verified", "post_activation_warning", "rollback_required", "rollback_executed"]]
        if not verified:
            return 0.0
        clean = sum(1 for a in verified if a.current_status == "post_activation_verified")
        return clean / len(verified)

    @staticmethod
    def calculate_rollback_after_activation_rate(adoptions: List[StableAdoptionRecord]) -> float:
        advanced = [a for a in adoptions if a.current_status in ["stable_pointer_advanced", "post_activation_verified", "post_activation_warning", "rollback_required", "rollback_executed", "adoption_completed"]]
        if not advanced:
            return 0.0
        rollbacks = sum(1 for a in advanced if a.current_status in ["rollback_required", "rollback_executed"])
        return rollbacks / len(advanced)
