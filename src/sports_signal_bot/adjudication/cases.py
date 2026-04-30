import uuid
from typing import List, Optional
from datetime import datetime

from .contracts import (
    AdjudicationCaseRecord,
    AdjudicationCaseFamily,
    AdjudicationSeverity,
    AdjudicationQueuePriority,
    AdjudicationCaseStatus
)

class AdjudicationCaseBuilder:
    @staticmethod
    def build_adjudication_case(
        case_type: AdjudicationCaseFamily,
        target_entity_type: str,
        target_entity_id: str,
        source_component: str,
        severity: AdjudicationSeverity,
        evidence_bundle_ref: str,
        dispute_refs: Optional[List[str]] = None,
        sport: Optional[str] = None,
        market_type: Optional[str] = None
    ) -> AdjudicationCaseRecord:

        priority = AdjudicationCaseBuilder.assign_case_priority(severity)

        return AdjudicationCaseRecord(
            case_id=str(uuid.uuid4()),
            case_type=case_type,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            sport=sport,
            market_type=market_type,
            source_component=source_component,
            severity=severity,
            evidence_bundle_ref=evidence_bundle_ref,
            dispute_refs=dispute_refs or [],
            current_status=AdjudicationCaseStatus.queued,
            queue_priority=priority,
            created_at=datetime.utcnow(),
            warnings=[]
        )

    @staticmethod
    def assign_case_priority(severity: AdjudicationSeverity) -> AdjudicationQueuePriority:
        if severity == AdjudicationSeverity.critical:
            return AdjudicationQueuePriority.urgent
        elif severity == AdjudicationSeverity.high:
            return AdjudicationQueuePriority.high
        elif severity == AdjudicationSeverity.medium:
            return AdjudicationQueuePriority.normal
        else:
            return AdjudicationQueuePriority.low
