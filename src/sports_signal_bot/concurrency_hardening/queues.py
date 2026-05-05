import uuid
import datetime
from typing import Dict, Any, List, Optional

from .contracts import (
    QueueDisciplineRecord, QueueSampleRecord, QueueOverflowRecord,
    QueueDrainRecord, BackpressureDecisionRecord, QueueHealthRecord,
    QueueManifestRecord, QueueWarningRecord
)

def build_queue_discipline(target_queue: str) -> QueueDisciplineRecord:
    """Builds a queue discipline record."""
    return QueueDisciplineRecord(
        discipline_id=f"qd_{uuid.uuid4().hex[:8]}",
        target_queue=target_queue,
        status="monitored",
        warnings=[]
    )

def sample_queue_pressure(queue_length: int) -> QueueSampleRecord:
    """Samples queue pressure."""
    return QueueSampleRecord(
        sample_id=f"samp_{uuid.uuid4().hex[:8]}",
        length=queue_length
    )

def detect_queue_overflow_or_starvation(discipline: QueueDisciplineRecord, sample: QueueSampleRecord, max_capacity: int) -> Optional[QueueOverflowRecord]:
    """Detects if queue is overflowing."""
    if sample.length > max_capacity:
        discipline.status = "overflowing"
        discipline.warnings.append(
            QueueWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Queue overflow: {sample.length} > {max_capacity}",
                severity="high"
            )
        )
        return QueueOverflowRecord(
            overflow_id=f"ovfl_{uuid.uuid4().hex[:8]}",
            dropped_items=sample.length - max_capacity
        )
    elif sample.length == 0:
         discipline.warnings.append(
            QueueWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Queue starvation: length is 0",
                severity="low"
            )
        )
    return None

def summarize_queue_health(disciplines: List[QueueDisciplineRecord]) -> QueueManifestRecord:
    """Summarizes queue health."""
    unhealthy = sum(1 for d in disciplines if d.status == "overflowing")

    health = QueueHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=unhealthy == 0,
        status_summary=f"Found {unhealthy} queues in overflow state."
    )

    return QueueManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        disciplines=disciplines,
        health=health
    )
