import datetime
import uuid
from typing import List

from .contracts import (
    ConcurrencyGuardConfig,
    ConcurrencyGuardHealthRecord,
    ConcurrencyGuardManifestRecord,
    ConcurrencyGuardRecord,
    ConcurrencyGuardWarningRecord,
)


def build_concurrency_guard(config: ConcurrencyGuardConfig) -> ConcurrencyGuardRecord:
    """Builds a ConcurrencyGuardRecord."""
    guard_id = f"cg_{uuid.uuid4().hex[:8]}"

    scope_id = f"scp_{uuid.uuid4().hex[:8]}"
    ownership_id = f"own_{uuid.uuid4().hex[:8]}"
    ordering_id = f"ord_{uuid.uuid4().hex[:8]}"
    timeout_id = f"to_{uuid.uuid4().hex[:8]}"
    cancellation_id = f"cx_{uuid.uuid4().hex[:8]}"

    warnings = []
    status = "guard_safe"

    if config.guard_family not in [
        "shared_state_guard",
        "async_join_guard",
        "ordering_guard",
        "stale_read_guard",
        "idempotency_guard",
        "queue_bound_guard",
        "write_once_guard",
        "side_effect_guard",
    ]:
        status = "guard_review_only"
        warnings.append(
            ConcurrencyGuardWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Unknown guard family: {config.guard_family}",
                severity="medium",
            )
        )

    if config.timeout_ms > 30000:  # Example rule
        status = "guard_caveated"
        warnings.append(
            ConcurrencyGuardWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Timeout unusually high: {config.timeout_ms}ms",
                severity="low",
            )
        )

    return ConcurrencyGuardRecord(
        concurrency_guard_id=guard_id,
        guard_family=config.guard_family,
        protected_surface_ref=config.protected_surface_ref,
        guard_scope_ref=scope_id,
        ownership_ref=ownership_id,
        ordering_ref=ordering_id,
        timeout_ref=timeout_id,
        cancellation_ref=cancellation_id,
        guard_status=status,
        warnings=warnings,
    )


def validate_guard_coverage(
    guards: List[ConcurrencyGuardRecord], surfaces: List[str]
) -> List[str]:
    """Validates that all critical surfaces are covered by guards."""
    covered = {g.protected_surface_ref for g in guards}
    return [s for s in surfaces if s not in covered]


def detect_unprotected_shared_state(
    guards: List[ConcurrencyGuardRecord], known_states: List[str]
) -> List[str]:
    """Detects shared state surfaces that lack a 'shared_state_guard'."""
    shared_state_guards = {
        g.protected_surface_ref
        for g in guards
        if g.guard_family == "shared_state_guard"
    }
    return [s for s in known_states if s not in shared_state_guards]


def summarize_concurrency_guards(
    guards: List[ConcurrencyGuardRecord],
) -> ConcurrencyGuardManifestRecord:
    """Summarizes concurrency guards into a manifest."""
    unhealthy_guards = [
        g.concurrency_guard_id
        for g in guards
        if g.guard_status not in ["guard_safe", "guard_caveated"]
    ]

    health = ConcurrencyGuardHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=len(unhealthy_guards) == 0,
        status_summary=f"Found {len(unhealthy_guards)} unhealthy guards out of {len(guards)} total.",
        failing_guards=unhealthy_guards,
    )

    return ConcurrencyGuardManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        guards=guards,
        health=health,
    )
