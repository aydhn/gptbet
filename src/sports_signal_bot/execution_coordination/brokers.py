import datetime
import uuid
from typing import List, Optional
from sports_signal_bot.execution_coordination.contracts import (
    ApprovalTokenBrokerRecord, TokenAllocationRecord, TokenReservationRecord,
    TokenBrokerStatus, TokenBrokerDecisionRecord
)

class ApprovalTokenBroker:
    def __init__(self, broker_policy_ref: str = "default_policy"):
        self.broker_id = f"brk_{uuid.uuid4().hex[:8]}"
        self.token_pool_refs = ["default_pool"]
        self.active_allocations: List[TokenAllocationRecord] = []
        self.pending_reservations: List[TokenReservationRecord] = []
        self.renewal_backlog = 0
        self.broker_policy_ref = broker_policy_ref
        self.health_status = TokenBrokerStatus.BROKER_HEALTHY
        self.warnings: List[str] = []

    def request_allocation(self, lane_ref: str, scope: str, step_quota: int = 100) -> TokenBrokerDecisionRecord:
        # Simple policy: allow if < 5 active allocations
        if len(self.active_allocations) < 5:
            allocation = TokenAllocationRecord(
                token_ref=f"tok_{uuid.uuid4().hex[:8]}",
                lane_ref=lane_ref,
                allocation_time=datetime.datetime.now(datetime.timezone.utc),
                allocation_scope=scope,
                remaining_window=3600,
                step_quota=step_quota,
                renewal_eligibility=True,
                preemption_eligibility=True,
                closure_dependency="none"
            )
            self.active_allocations.append(allocation)
            return TokenBrokerDecisionRecord(
                decision_id=f"dec_{uuid.uuid4().hex[:8]}",
                lane_ref=lane_ref,
                granted=True,
                allocation=allocation,
                reason="Capacity available"
            )
        else:
            self.health_status = TokenBrokerStatus.BROKER_TOKEN_PRESSURE
            return TokenBrokerDecisionRecord(
                decision_id=f"dec_{uuid.uuid4().hex[:8]}",
                lane_ref=lane_ref,
                granted=False,
                reason="Token pressure high"
            )

    def revoke_allocation(self, lane_ref: str):
         self.active_allocations = [a for a in self.active_allocations if a.lane_ref != lane_ref]

    def get_summary(self) -> ApprovalTokenBrokerRecord:
        return ApprovalTokenBrokerRecord(
            broker_id=self.broker_id,
            token_pool_refs=self.token_pool_refs,
            active_allocations=self.active_allocations.copy(),
            pending_reservations=self.pending_reservations.copy(),
            renewal_backlog=self.renewal_backlog,
            broker_policy_ref=self.broker_policy_ref,
            health_status=self.health_status,
            warnings=self.warnings.copy()
        )
