import uuid
from typing import Dict, Any, List
from .contracts import PolicyChangeRequestRecord, PolicyReviewRecord

class PolicyReviewPipeline:
    def __init__(self):
        self.requests: Dict[str, PolicyChangeRequestRecord] = {}
        self.reviews: Dict[str, PolicyReviewRecord] = {}

    def create_change_request(self, bundle_id: str, proposed_changes: Dict[str, Any], affected_scopes: List[str]) -> PolicyChangeRequestRecord:
        req = PolicyChangeRequestRecord(
            request_id=f"pcr_{uuid.uuid4().hex[:8]}",
            bundle_id=bundle_id,
            proposed_changes=proposed_changes,
            affected_scopes=affected_scopes
        )
        self.requests[req.request_id] = req
        return req

    def submit_review(self, request_id: str, reviewer_id: str, decision: str, checklist: Dict[str, bool], comments: str) -> PolicyReviewRecord:
        review = PolicyReviewRecord(
            review_id=f"rev_{uuid.uuid4().hex[:8]}",
            request_id=request_id,
            reviewer_id=reviewer_id,
            checklist_results=checklist,
            decision=decision,
            comments=comments
        )
        self.reviews[review.review_id] = review

        try:
            self.requests[request_id].status = "reviewed"
        except KeyError:
            pass

        return review
