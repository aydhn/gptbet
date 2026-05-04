from typing import List
from .contracts import ContextSectionRecord

# Section Families
SECTION_FEDERATED_TRACE = "federated_trace_section"
SECTION_PROOF_FRESHNESS = "proof_freshness_section"
SECTION_OBSERVATORY_EXCHANGE = "observatory_exchange_section"
SECTION_REPLAY_AND_DEBT = "replay_and_debt_section"
SECTION_SETTLEMENT_PROGRESS = "settlement_progress_section"
SECTION_SOVEREIGNTY_WARNING = "sovereignty_warning_section"
SECTION_NO_SAFE_VISIBILITY = "no_safe_visibility_section"
SECTION_STALE_STATE = "stale_state_section"
SECTION_CAVEAT_SUMMARY = "caveat_summary_section"
SECTION_ACTION_CONTEXT = "action_context_section"
SECTION_DEGRADED_PATH = "degraded_path_section"

def build_context_section(family: str, content: str) -> ContextSectionRecord:
    import uuid
    return ContextSectionRecord(
        section_id=f"sec_{uuid.uuid4().hex[:8]}",
        family=family,
        content=content
    )
