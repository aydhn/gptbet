import datetime
import uuid
from typing import List, Dict, Optional
from src.sports_signal_bot.execution_coordination.contracts import (
    LaneScheduleRecord, ScheduleStatus, PriorityBand, SchedulingWindowRecord, MultiLaneSchedulerRecord
)

class MultiLaneScheduler:
    def __init__(self):
        self.scheduler_id = f"sch_{uuid.uuid4().hex[:8]}"
        self.active_schedules: List[LaneScheduleRecord] = []
        self.waiting_schedules: List[LaneScheduleRecord] = []
        self.completed_schedules: List[LaneScheduleRecord] = []

    def submit_lane(self, lane_ref: str, priority_band: PriorityBand, requested_window: SchedulingWindowRecord) -> LaneScheduleRecord:
        record = LaneScheduleRecord(
            schedule_id=f"sched_{uuid.uuid4().hex[:8]}",
            lane_ref=lane_ref,
            requested_runtime_window=requested_window,
            priority_band=priority_band,
            contention_status="clear",
            token_status="pending",
            closure_dependency_status="clear",
            schedule_status=ScheduleStatus.SCHEDULE_REQUESTED
        )
        self.waiting_schedules.append(record)
        return record

    def admit_schedule(self, schedule_id: str):
        for s in self.waiting_schedules:
            if s.schedule_id == schedule_id:
                s.schedule_status = ScheduleStatus.SCHEDULE_ADMITTED

    def assign_runtime_window(self, schedule_id: str, window: SchedulingWindowRecord):
        for s in self.waiting_schedules:
            if s.schedule_id == schedule_id:
                s.assigned_runtime_window = window
                s.schedule_status = ScheduleStatus.SCHEDULE_RUNTIME_ASSIGNED
                self.waiting_schedules.remove(s)
                self.active_schedules.append(s)
                break

    def defer_schedule(self, schedule_id: str, reason: str):
        for s in self.waiting_schedules:
            if s.schedule_id == schedule_id:
                s.schedule_status = ScheduleStatus.SCHEDULE_WAITING_ARBITRATION
                s.warnings.append(f"Deferred: {reason}")

    def complete_schedule(self, schedule_id: str):
        for s in self.active_schedules:
            if s.schedule_id == schedule_id:
                s.schedule_status = ScheduleStatus.SCHEDULE_COMPLETED
                self.active_schedules.remove(s)
                self.completed_schedules.append(s)
                break

    def get_summary(self) -> MultiLaneSchedulerRecord:
        return MultiLaneSchedulerRecord(
            scheduler_id=self.scheduler_id,
            active_schedules=self.active_schedules.copy(),
            waiting_schedules=self.waiting_schedules.copy(),
            completed_schedules=self.completed_schedules.copy()
        )
