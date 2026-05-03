import pytest
from src.sports_signal_bot.execution_coordination.fabric import SupervisedExecutionCoordinationFabric
from src.sports_signal_bot.execution_coordination.strategies.conservative import ConservativeCoordinationFabricStrategy
from src.sports_signal_bot.execution_coordination.contracts import PriorityBand, SchedulingWindowRecord
import datetime

def test_conservative_arbitration_forces_serialization():
    strategy = ConservativeCoordinationFabricStrategy()
    fabric = SupervisedExecutionCoordinationFabric(strategy=strategy)

    window = SchedulingWindowRecord(
        window_id="test_win",
        start_time=datetime.datetime.now(datetime.timezone.utc),
        end_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        max_parallel_lanes=2
    )

    fabric.admit_lane("lane_1", PriorityBand.CRITICAL_RECOVERY, window)
    fabric.admit_lane("lane_2", PriorityBand.CRITICAL_RECOVERY, window)

    # Run coordinate, which should detect contention since there are >1 lanes waiting
    fabric.coordinate()

    # Conservative strategy serializes, so lane_1 wins, lane_2 gets deferred
    assert len(fabric.scheduler.active_schedules) == 1
    assert fabric.scheduler.active_schedules[0].lane_ref == "lane_1"

    assert len(fabric.scheduler.waiting_schedules) == 1
    assert fabric.scheduler.waiting_schedules[0].lane_ref == "lane_2"
    assert fabric.scheduler.waiting_schedules[0].schedule_status == "schedule_waiting_arbitration"
