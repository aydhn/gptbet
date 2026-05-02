from typing import Dict, List, Callable
from datetime import datetime, timezone
from .contracts import DiscoveryEventRecord, EventEnvelopeRecord, EventCursorRecord
import hashlib

class DiscoveryEventBus:
    def __init__(self):
        self.topics: Dict[str, List[EventEnvelopeRecord]] = {}
        self.cursors: Dict[str, Dict[str, int]] = {} # topic -> consumer_id -> index
        self.consumers: Dict[str, List[Callable]] = {} # topic -> list of callbacks

    def register_topic(self, topic: str):
        if topic not in self.topics:
            self.topics[topic] = []
            self.cursors[topic] = {}
            self.consumers[topic] = []

    def subscribe(self, topic: str, consumer_id: str, callback: Callable):
        self.register_topic(topic)
        if consumer_id not in self.cursors[topic]:
            self.cursors[topic][consumer_id] = 0
        self.consumers[topic].append((consumer_id, callback))

    def publish(self, event: DiscoveryEventRecord) -> EventEnvelopeRecord:
        self.register_topic(event.topic_ref)

        sequence_index = len(self.topics[event.topic_ref])
        event_hash = hashlib.sha256(f"{event.event_id}{sequence_index}".encode()).hexdigest()

        envelope = EventEnvelopeRecord(
            topic=event.topic_ref,
            event_family=event.event_family,
            source=event.source_ref,
            event_hash=event_hash,
            sequence_index=sequence_index,
            event=event,
            observability_tags={"published_at": datetime.now(timezone.utc).isoformat()}
        )

        self.topics[event.topic_ref].append(envelope)
        return envelope

    def dispatch_pending(self):
        for topic, envelopes in self.topics.items():
            for consumer_id, callback in self.consumers[topic]:
                current_cursor = self.cursors[topic].get(consumer_id, 0)
                while current_cursor < len(envelopes):
                    try:
                        callback(envelopes[current_cursor].event)
                        current_cursor += 1
                        self.cursors[topic][consumer_id] = current_cursor
                    except Exception as e:
                        # Resilient dispatch: log and halt this consumer's progress, but don't crash bus
                        print(f"Consumer {consumer_id} failed on topic {topic}: {e}")
                        break

    def get_consumer_cursor(self, topic: str, consumer_id: str) -> EventCursorRecord:
        current_idx = self.cursors.get(topic, {}).get(consumer_id, 0)
        total_events = len(self.topics.get(topic, []))
        lag = total_events - current_idx

        last_event_id = "none"
        if current_idx > 0 and len(self.topics.get(topic, [])) >= current_idx:
            last_event_id = self.topics[topic][current_idx - 1].event.event_id

        return EventCursorRecord(
            consumer_id=consumer_id,
            topic_ref=topic,
            last_processed_event_id=last_event_id,
            lag_events_count=lag,
            last_processed_at=datetime.now(timezone.utc),
            is_stalled=lag > 50  # Arbitrary threshold for stalling
        )
