import pytest
import datetime
from src.sports_signal_bot.execution_coordination.contracts import PriorityBand, SchedulingWindowRecord, ScheduleStatus
from src.sports_signal_bot.execution_coordination.schedulers import MultiLaneScheduler

def test_multi_lane_scheduler_submit():
    scheduler = MultiLaneScheduler()
    window = SchedulingWindowRecord(
        window_id="test_win",
        start_time=datetime.datetime.now(datetime.timezone.utc),
        end_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        max_parallel_lanes=1
    )

    schedule = scheduler.submit_lane("lane_1", PriorityBand.CRITICAL_RECOVERY, window)

    assert schedule.schedule_status == ScheduleStatus.SCHEDULE_REQUESTED
    assert len(scheduler.waiting_schedules) == 1
    assert scheduler.waiting_schedules[0].lane_ref == "lane_1"

def test_multi_lane_scheduler_assign_window():
    scheduler = MultiLaneScheduler()
    window = SchedulingWindowRecord(
        window_id="test_win",
        start_time=datetime.datetime.now(datetime.timezone.utc),
        end_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        max_parallel_lanes=1
    )

    schedule = scheduler.submit_lane("lane_1", PriorityBand.CRITICAL_RECOVERY, window)
    scheduler.assign_runtime_window(schedule.schedule_id, window)

    assert len(scheduler.waiting_schedules) == 0
    assert len(scheduler.active_schedules) == 1
    assert scheduler.active_schedules[0].schedule_status == ScheduleStatus.SCHEDULE_RUNTIME_ASSIGNED
