import pytest
from sports_signal_bot.streaming_discovery.contracts import DiscoveryEventRecord
from sports_signal_bot.streaming_discovery.bus import DiscoveryEventBus
from sports_signal_bot.streaming_discovery.anomaly_clusters import AnomalyClusterer
from sports_signal_bot.streaming_discovery.adaptation import AdaptiveTrustRouter
from sports_signal_bot.streaming_discovery.strategies.balanced_observability import BalancedObservabilityFabricStrategy
from sports_signal_bot.streaming_discovery.topics import StreamTopic
from sports_signal_bot.streaming_discovery.events import EventFamily

def test_discovery_event_bus():
    bus = DiscoveryEventBus()
    received = []

    def dummy_consumer(event):
        received.append(event)

    bus.subscribe(StreamTopic.SYNC_EVENTS.value, "test_consumer", dummy_consumer)

    event = DiscoveryEventRecord(event_family=EventFamily.SYNC_SUCCEEDED.value, topic_ref=StreamTopic.SYNC_EVENTS.value, source_ref="test_src")
    bus.publish(event)

    bus.dispatch_pending()
    assert len(received) == 1
    assert received[0].source_ref == "test_src"

    cursor = bus.get_consumer_cursor(StreamTopic.SYNC_EVENTS.value, "test_consumer")
    assert cursor.lag_events_count == 0

def test_anomaly_clustering():
    clusterer = AnomalyClusterer()

    # 3 failures should trigger a high severity cluster
    for _ in range(3):
        clusterer.process_event(DiscoveryEventRecord(
            event_family=EventFamily.SYNC_FAILED.value,
            topic_ref=StreamTopic.SYNC_EVENTS.value,
            source_ref="bad_source"
        ))

    clusters = clusterer.get_clusters()
    assert len(clusters) == 1
    assert clusters[0].severity == "high"
    assert "bad_source" in clusters[0].affected_sources

def test_adaptive_routing():
    strategy = BalancedObservabilityFabricStrategy()
    router = AdaptiveTrustRouter(profile=strategy.get_profile())
    router.set_baseline("test_src", 1.0)

    router.process_event(DiscoveryEventRecord(
        event_family=EventFamily.TRUST_DOWNGRADED.value,
        topic_ref=StreamTopic.TRUST_EVENTS.value,
        source_ref="test_src"
    ))

    # Trust should be reduced
    assert router.route_weights["test_src"] < 1.0
    history = router.get_history()
    assert len(history) == 1
    assert history[0].adaptation_outcome == "trust_adjusted"
