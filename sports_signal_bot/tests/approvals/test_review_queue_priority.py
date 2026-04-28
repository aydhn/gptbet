from sports_signal_bot.approvals.review_queue import assign_review_priority, sort_review_queue
from sports_signal_bot.approvals.contracts import ReviewItemRecord, ReviewItemType

def test_review_priority_assignment():
    assert assign_review_priority("critical", "some_request") == "critical"
    assert assign_review_priority("low", "approve_freeze_release") == "critical"
    assert assign_review_priority("high", "approve_refresh_plan") == "high"
    assert assign_review_priority("low", "approve_mode_switch") == "low"

def test_sort_review_queue():
    items = [
        ReviewItemRecord(review_id="3", priority="low", category=ReviewItemType.decision_review_item, title="", summary="", request_ref="", risk_level=""),
        ReviewItemRecord(review_id="1", priority="critical", category=ReviewItemType.decision_review_item, title="", summary="", request_ref="", risk_level=""),
        ReviewItemRecord(review_id="2", priority="high", category=ReviewItemType.decision_review_item, title="", summary="", request_ref="", risk_level=""),
    ]
    sorted_items = sort_review_queue(items)
    assert sorted_items[0].review_id == "1"
    assert sorted_items[1].review_id == "2"
    assert sorted_items[2].review_id == "3"
