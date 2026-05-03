import pytest
from src.sports_signal_bot.execution_coordination.fabric import SupervisedExecutionCoordinationFabric
from src.sports_signal_bot.execution_coordination.strategies.rollback_closure_priority import RollbackClosurePriorityStrategy
from src.sports_signal_bot.execution_coordination.contracts import PriorityBand, SchedulingWindowRecord, FabricStatus
import datetime

def test_rollback_priority_strategy_defers_normal_lanes():
    strategy = RollbackClosurePriorityStrategy()
    fabric = SupervisedExecutionCoordinationFabric(strategy=strategy)

    window = SchedulingWindowRecord(
        window_id="test_win",
        start_time=datetime.datetime.now(datetime.timezone.utc),
        end_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        max_parallel_lanes=2
    )

    fabric.admit_lane("lane_rollback_1", PriorityBand.ROLLBACK_PRIORITY, window)
    fabric.admit_lane("lane_normal_2", PriorityBand.REPAIR_PRIORITY, window)

    fabric.coordinate()

    # Rollback should win the contention arbitration
    assert len(fabric.scheduler.active_schedules) == 1
    assert fabric.scheduler.active_schedules[0].lane_ref == "lane_rollback_1"

    assert len(fabric.scheduler.waiting_schedules) == 1
    assert fabric.scheduler.waiting_schedules[0].lane_ref == "lane_normal_2"

def test_rollback_priority_status_computation():
    strategy = RollbackClosurePriorityStrategy()

    # Simulate high backlog pressure
    status = strategy.compute_fabric_status(active_contentions=1, backlog_pressure=0.8, token_broker_status="broker_healthy")

    assert status == FabricStatus.FABRIC_ROLLBACK_PRIORITY_MODE
