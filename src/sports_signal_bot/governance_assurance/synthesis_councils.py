from typing import List, Dict, Any, Optional
from datetime import datetime
from sports_signal_bot.governance_assurance.contracts import (
    ResilienceSynthesisCouncilRecord,
    SynthesisCouncilCaseRecord,
    CouncilFamily,
    CaseStatus,
    SynthesisCouncilWarningRecord
)

def build_resilience_synthesis_council(
    council_id: str,
    council_family: CouncilFamily,
    governed_refs: List[str]
) -> ResilienceSynthesisCouncilRecord:
    """Builds a new resilience synthesis council."""
    return ResilienceSynthesisCouncilRecord(
        synthesis_council_id=council_id,
        council_family=council_family,
        governed_synthesis_refs=governed_refs,
        participant_refs=[],
        quorum_policy_ref="default_quorum_policy",
        precedence_policy_ref="default_precedence_policy",
        backlog_ref=f"backlog_{council_id}",
        health_status="healthy",
        warnings=[]
    )

def summarize_synthesis_council(council: ResilienceSynthesisCouncilRecord) -> Dict[str, Any]:
    """Provides a bounded summary of the council's state."""
    return {
        "council_id": council.synthesis_council_id,
        "family": council.council_family.value,
        "governed_syntheses": len(council.governed_synthesis_refs),
        "health": council.health_status,
        "warnings_count": len(council.warnings)
    }
