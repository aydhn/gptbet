import uuid
import datetime
from typing import Dict, Any, List, Optional

from .contracts import (
    AsyncOrderingRecord, OrderingDependencyRecord, OrderingBarrierRecord,
    OrderingViolationRecord, OrderingRecoveryRecord, OrderingParityRecord,
    OrderingHealthRecord, OrderingManifestRecord, OrderingWarningRecord
)

def build_async_ordering_graph(
    target_ref: str,
    rules: Dict[str, Any]
) -> AsyncOrderingRecord:
    """Builds an AsyncOrderingRecord representing an ordering graph."""
    ordering_id = f"ord_{uuid.uuid4().hex[:8]}"
    warnings = []
    status = "ordering_safe"

    # Simple validation rule
    if "deterministic_merge" not in rules or not rules["deterministic_merge"]:
        status = "ordering_caveated"
        warnings.append(
            OrderingWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message="Missing deterministic merge policy in rules.",
                severity="medium"
            )
        )

    return AsyncOrderingRecord(
        ordering_id=ordering_id,
        target_ref=target_ref,
        rules=rules,
        status=status,
        warnings=warnings
    )

def validate_async_ordering(ordering: AsyncOrderingRecord, execution_trace: List[str]) -> bool:
    """Validates an execution trace against ordering rules."""
    # Simplified simulation: check if trace meets some expected sequence in rules
    expected_sequence = ordering.rules.get("expected_sequence", [])
    if not expected_sequence:
        return True # Nothing to check

    # Check if expected items appear in order (allows gaps)
    trace_idx = 0
    for expected in expected_sequence:
        found = False
        while trace_idx < len(execution_trace):
            if execution_trace[trace_idx] == expected:
                found = True
                trace_idx += 1
                break
            trace_idx += 1
        if not found:
            return False

    return True

def detect_ordering_violation(ordering: AsyncOrderingRecord, execution_trace: List[str]) -> Optional[OrderingViolationRecord]:
    """Detects ordering violations."""
    if validate_async_ordering(ordering, execution_trace):
        return None

    return OrderingViolationRecord(
        violation_id=f"viol_{uuid.uuid4().hex[:8]}",
        description=f"Trace {execution_trace} violated ordering rules for {ordering.target_ref}"
    )

def summarize_async_ordering(orderings: List[AsyncOrderingRecord]) -> OrderingManifestRecord:
    """Summarizes async orderings into a manifest."""
    unhealthy = [o.ordering_id for o in orderings if o.status not in ["ordering_safe"]]

    health = OrderingHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=len(unhealthy) == 0,
        status_summary=f"Found {len(unhealthy)} orderings with issues out of {len(orderings)} total."
    )

    return OrderingManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        orderings=orderings,
        health=health
    )
