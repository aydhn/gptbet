from enum import Enum

class StreamTopic(str, Enum):
    SYNC_EVENTS = "sync_events"
    OVERLAY_EVENTS = "overlay_events"
    ROUTING_EVENTS = "routing_events"
    TRUST_EVENTS = "trust_events"
    FRESHNESS_EVENTS = "freshness_events"
    SUPERSESSION_EVENTS = "supersession_events"
    QUARANTINE_EVENTS = "quarantine_events"
    ANOMALY_EVENTS = "anomaly_events"
    TELEMETRY_EVENTS = "telemetry_events"
