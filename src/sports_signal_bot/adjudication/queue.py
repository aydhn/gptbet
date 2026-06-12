import uuid
from typing import Dict, List, Optional

from .contracts import (
    AdjudicationCaseRecord,
    AdjudicationCaseStatus,
    AdjudicationQueuePriority,
    AdjudicationQueueRecord,
)


class AdjudicationRegistry:
    def __init__(self):
        self.cases: Dict[str, AdjudicationCaseRecord] = {}

    def register_case(self, case: AdjudicationCaseRecord) -> None:
        self.cases[case.case_id] = case

    def get_case(self, case_id: str) -> Optional[AdjudicationCaseRecord]:
        return self.cases.get(case_id)

    def update_case(self, case: AdjudicationCaseRecord) -> None:
        if case.case_id in self.cases:
            self.cases[case.case_id] = case

    def list_cases(self) -> List[AdjudicationCaseRecord]:
        return list(self.cases.values())


class AdjudicationQueueBuilder:
    def __init__(self, registry: AdjudicationRegistry):
        self.registry = registry

    def build_queue(
        self,
        priority: Optional[AdjudicationQueuePriority] = None,
        status: AdjudicationCaseStatus = AdjudicationCaseStatus.queued,
    ) -> AdjudicationQueueRecord:
        cases = []
        for case in self.registry.list_cases():
            if case.current_status == status:
                if priority is None or case.queue_priority == priority:
                    cases.append(case)

        # sort by priority (urgent, high, normal, low) and then by created_at
        priority_map = {
            AdjudicationQueuePriority.urgent: 0,
            AdjudicationQueuePriority.high: 1,
            AdjudicationQueuePriority.normal: 2,
            AdjudicationQueuePriority.low: 3,
        }

        cases.sort(key=lambda x: (priority_map[x.queue_priority], x.created_at))

        return AdjudicationQueueRecord(queue_id=str(uuid.uuid4()), cases=cases)

    def route_case_to_queue(self, case: AdjudicationCaseRecord) -> None:
        # In a real system, this might publish to Kafka/RabbitMQ.
        # Here we just ensure it's registered and marked as queued.
        case.current_status = AdjudicationCaseStatus.queued
        self.registry.register_case(case)

    def summarize_queue_pressure(self) -> Dict[str, int]:
        pressure = {p.value: 0 for p in AdjudicationQueuePriority}
        for case in self.registry.list_cases():
            if case.current_status == AdjudicationCaseStatus.queued:
                pressure[case.queue_priority.value] += 1
        return pressure

    def detect_duplicate_case_submission(
        self, new_case: AdjudicationCaseRecord
    ) -> bool:
        for case in self.registry.list_cases():
            if case.current_status not in [
                AdjudicationCaseStatus.resolved,
                AdjudicationCaseStatus.archived,
            ]:
                if (
                    case.case_type == new_case.case_type
                    and case.target_entity_type == new_case.target_entity_type
                    and case.target_entity_id == new_case.target_entity_id
                ):
                    return True
        return False
