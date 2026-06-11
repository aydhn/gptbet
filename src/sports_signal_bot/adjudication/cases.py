import uuid
from datetime import datetime

from .contracts import (AdjudicationCaseCreationRequest,
                        AdjudicationCaseRecord, AdjudicationCaseStatus,
                        AdjudicationQueuePriority, AdjudicationSeverity)


class AdjudicationCaseBuilder:
    @staticmethod
    def build_adjudication_case(
        request: AdjudicationCaseCreationRequest,
    ) -> AdjudicationCaseRecord:

        priority = AdjudicationCaseBuilder.assign_case_priority(request.severity)

        return AdjudicationCaseRecord(
            case_id=str(uuid.uuid4()),
            case_type=request.case_type,
            target_entity_type=request.target_entity_type,
            target_entity_id=request.target_entity_id,
            sport=request.sport,
            market_type=request.market_type,
            source_component=request.source_component,
            severity=request.severity,
            evidence_bundle_ref=request.evidence_bundle_ref,
            dispute_refs=request.dispute_refs or [],
            current_status=AdjudicationCaseStatus.queued,
            queue_priority=priority,
            created_at=datetime.utcnow(),
            warnings=[],
        )

    @staticmethod
    def assign_case_priority(
        severity: AdjudicationSeverity,
    ) -> AdjudicationQueuePriority:
        if severity == AdjudicationSeverity.critical:
            return AdjudicationQueuePriority.urgent
        elif severity == AdjudicationSeverity.high:
            return AdjudicationQueuePriority.high
        elif severity == AdjudicationSeverity.medium:
            return AdjudicationQueuePriority.normal
        else:
            return AdjudicationQueuePriority.low
