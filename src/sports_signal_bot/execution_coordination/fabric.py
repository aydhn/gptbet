import uuid
from typing import List, Optional
from src.sports_signal_bot.execution_coordination.contracts import (
    ExecutionCoordinationFabricRecord, FabricStatus, CoordinationHealthRecord, PriorityBand, SchedulingWindowRecord
)
from src.sports_signal_bot.execution_coordination.schedulers import MultiLaneScheduler
from src.sports_signal_bot.execution_coordination.brokers import ApprovalTokenBroker
from src.sports_signal_bot.execution_coordination.contentions import ContentionDetector
from src.sports_signal_bot.execution_coordination.arbitration import ArbitrationEngine
from src.sports_signal_bot.execution_coordination.ledgers import CoordinationLedger
from src.sports_signal_bot.execution_coordination.strategies import BaseCoordinationStrategy, BalancedMultiLaneFabricStrategy
import datetime

class SupervisedExecutionCoordinationFabric:
    def __init__(self, strategy: Optional[BaseCoordinationStrategy] = None):
        self.fabric_id = f"fab_{uuid.uuid4().hex[:8]}"
        self.strategy = strategy or BalancedMultiLaneFabricStrategy()
        self.scheduler = MultiLaneScheduler()
        self.broker = ApprovalTokenBroker()
        self.contention_detector = ContentionDetector()
        self.arbitration_engine = ArbitrationEngine(strategy=self.strategy)
        self.ledger = CoordinationLedger()
        self.status = FabricStatus.FABRIC_NORMAL
        self.warnings: List[str] = []

    def admit_lane(self, lane_ref: str, priority_band: PriorityBand, requested_window: SchedulingWindowRecord):
        self.ledger.append_entry(lane_ref, "lane_submitted", {"priority": priority_band})
        schedule = self.scheduler.submit_lane(lane_ref, priority_band, requested_window)
        self.ledger.append_entry(lane_ref, "schedule_requested", {"schedule_id": schedule.schedule_id})
        return schedule

    def request_allocation(self, lane_ref: str, scope: str):
        self.ledger.append_entry(lane_ref, "broker_reservation_requested", {"scope": scope})
        decision = self.broker.request_allocation(lane_ref, scope)
        if decision.granted:
            self.ledger.append_entry(lane_ref, "token_allocated", {"decision_id": decision.decision_id})
        else:
             self.ledger.append_entry(lane_ref, "token_denied", {"decision_id": decision.decision_id, "reason": decision.reason})
        return decision

    def coordinate(self):
        # 1. Detect contentions among waiting schedules
        waiting_lane_refs = [s.lane_ref for s in self.scheduler.waiting_schedules]
        # simplified mock shared surface assumption
        shared_surfaces = ["shared_db"] if len(waiting_lane_refs) > 1 else []

        new_contentions = self.contention_detector.detect_contentions(waiting_lane_refs, shared_surfaces)
        for contention in new_contentions:
            for ref in contention.involved_lane_refs:
                self.ledger.append_entry(ref, "contention_opened", {"contention_id": contention.contention_id})

            # 2. Arbitrate
            decision = self.arbitration_engine.arbitrate(contention, self.scheduler.active_schedules)
            for ref in decision.winning_lane_refs:
                self.ledger.append_entry(ref, "arbitration_decided", {"outcome": "win", "decision_id": decision.arbitration_id})
            for ref in decision.deferred_lane_refs:
                self.ledger.append_entry(ref, "arbitration_decided", {"outcome": "deferred", "decision_id": decision.arbitration_id})
                # Find matching schedule and defer
                for s in self.scheduler.waiting_schedules:
                    if s.lane_ref == ref:
                         self.scheduler.defer_schedule(s.schedule_id, decision.reason)

            self.contention_detector.resolve_contention(contention.contention_id, decision.arbitration_id)

        # 3. Process remaining waiting schedules
        for s in list(self.scheduler.waiting_schedules):
             if s.schedule_status != "schedule_waiting_arbitration":
                  self.scheduler.admit_schedule(s.schedule_id)
                  # Request token
                  token_decision = self.request_allocation(s.lane_ref, "live_exec")
                  if token_decision.granted:
                       # Assign window
                       window = SchedulingWindowRecord(
                           window_id=f"win_{uuid.uuid4().hex[:8]}",
                           start_time=datetime.datetime.now(datetime.timezone.utc),
                           end_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
                           max_parallel_lanes=1
                       )
                       self.scheduler.assign_runtime_window(s.schedule_id, window)
                       self.ledger.append_entry(s.lane_ref, "runtime_window_assigned", {"window_id": window.window_id})
                       self.ledger.append_entry(s.lane_ref, "lane_started", {})
                  else:
                       self.scheduler.defer_schedule(s.schedule_id, "Token denied")

        # 4. Update fabric status
        active_contentions_count = len([c for c in self.contention_detector.active_contentions if c.current_resolution_state == "unresolved"])
        self.status = self.strategy.compute_fabric_status(active_contentions_count, 0.0, self.broker.health_status)

    def get_summary(self) -> ExecutionCoordinationFabricRecord:
        return ExecutionCoordinationFabricRecord(
            fabric_id=self.fabric_id,
            active_lane_refs=[s.lane_ref for s in self.scheduler.active_schedules],
            queue_refs=[s.lane_ref for s in self.scheduler.waiting_schedules],
            scheduler_ref=self.scheduler.scheduler_id,
            token_broker_ref=self.broker.broker_id,
            contention_refs=[c.contention_id for c in self.contention_detector.active_contentions],
            arbitration_refs=[d.arbitration_id for d in self.arbitration_engine.arbitration_history],
            coordination_status=self.status,
            warnings=self.warnings.copy()
        )

    def get_health(self) -> CoordinationHealthRecord:
        return CoordinationHealthRecord(
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            fabric_status=self.status,
            active_schedules=len(self.scheduler.active_schedules),
            waiting_schedules=len(self.scheduler.waiting_schedules),
            active_contentions=len([c for c in self.contention_detector.active_contentions if c.current_resolution_state == "unresolved"]),
            backlog_pressure_score=0.0,
            warnings=self.warnings.copy()
        )
