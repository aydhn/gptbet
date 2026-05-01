import uuid
from typing import Dict, Any, List
from .contracts import PolicyBundleRecord, PolicyPromotionRecord, PolicyReviewStatus

class PolicyPromotionManager:
    def promote_bundle(self, bundle: PolicyBundleRecord, to_status: PolicyReviewStatus, approvers: List[str]) -> PolicyPromotionRecord:
        record = PolicyPromotionRecord(
            promotion_id=f"promo_{uuid.uuid4().hex[:8]}",
            bundle_id=bundle.policy_bundle_id,
            from_status=bundle.status,
            to_status=to_status,
            approved_by=approvers
        )
        bundle.status = to_status
        return record
