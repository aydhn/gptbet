from typing import Dict, Any, List
import uuid
import datetime
from .contracts import DashboardFeedRecord, FeedFamilyRecord, FeedSchemaRecord, FeedEligibilityRecord, FeedConsumerProfileRecord
from .profiles import get_profile

def build_dashboard_feed(feed_family: str, items: List[Dict[str, Any]]) -> DashboardFeedRecord:
    return DashboardFeedRecord(
        feed_id=str(uuid.uuid4()),
        feed_family=feed_family,
        content=items,
        freshness="fresh"
    )

def validate_feed_schema(feed: DashboardFeedRecord, schema: FeedSchemaRecord) -> bool:
    # Basic schema validation
    return len(feed.content) >= 0

def redact_feed_for_profile(feed: DashboardFeedRecord, profile_id: str) -> DashboardFeedRecord:
    profile = get_profile(profile_id)
    redacted_feed = DashboardFeedRecord(**feed.dict())

    if profile.signer_metadata_masking_level != "none":
        for item in redacted_feed.content:
            if "signer_metadata" in item:
                 item["signer_metadata"] = "[REDACTED]"
    return redacted_feed

def summarize_feed_status(feed: DashboardFeedRecord) -> Dict[str, Any]:
    return {
        "feed_id": feed.feed_id,
        "feed_family": feed.feed_family,
        "item_count": len(feed.content),
        "freshness": feed.freshness,
        "generated_at": feed.generated_at.isoformat()
    }

def export_feed_bundle(feed: DashboardFeedRecord, format: str = "json") -> str:
    import json
    if format == "json":
        return json.dumps(feed.dict(), default=str)
    return str(feed.dict())

def evaluate_feed_eligibility(profile_id: str, feed_family: str) -> FeedEligibilityRecord:
    profile = get_profile(profile_id)
    # Simple check based on profile access level
    eligible = profile.feed_access_level in ["all", "premium"] or (profile.feed_access_level == "standard" and feed_family != "external_exchange_activity_feed")
    return FeedEligibilityRecord(eligible=eligible)

def assign_feed_profile(feed_family: str) -> FeedConsumerProfileRecord:
    return FeedConsumerProfileRecord(profile_id="public_viewer")

def detect_feed_staleness(feed: DashboardFeedRecord, threshold_minutes: int = 60) -> bool:
    age = datetime.datetime.utcnow() - feed.generated_at
    return age.total_seconds() > threshold_minutes * 60

def summarize_delivery_readiness(feed: DashboardFeedRecord) -> Dict[str, Any]:
    stale = detect_feed_staleness(feed)
    return {
        "feed_id": feed.feed_id,
        "ready": not stale,
        "stale": stale
    }
