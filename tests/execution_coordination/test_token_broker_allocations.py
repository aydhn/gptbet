import pytest
from sports_signal_bot.execution_coordination.brokers import ApprovalTokenBroker
from sports_signal_bot.execution_coordination.contracts import TokenBrokerStatus

def test_token_broker_allocation():
    broker = ApprovalTokenBroker()
    decision = broker.request_allocation("lane_1", "test_scope")

    assert decision.granted is True
    assert decision.allocation is not None
    assert decision.allocation.lane_ref == "lane_1"
    assert len(broker.active_allocations) == 1

def test_token_broker_pressure():
    broker = ApprovalTokenBroker()
    # Fill capacity (limit is 5 in mock)
    for i in range(5):
        broker.request_allocation(f"lane_{i}", "test_scope")

    decision = broker.request_allocation("lane_over", "test_scope")
    assert decision.granted is False
    assert broker.health_status == TokenBrokerStatus.BROKER_TOKEN_PRESSURE
