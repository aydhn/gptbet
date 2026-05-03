from typing import List, Dict, Any
import uuid
from .contracts import RemediationPlaybookRecord, PlaybookStepRecord, PlaybookPrerequisiteRecord, PlaybookRiskRecord, PlaybookRollbackNoteRecord, FailurePatternRecord, PatternSimilarityRecord

def build_playbook_steps(target_family: str) -> List[PlaybookStepRecord]:
    if target_family == "quarantine_recovery":
        return [
            PlaybookStepRecord(
                step_order=1,
                step_family="isolate_source",
                rationale="Prevent contaminated data from spreading.",
                safety_bounds="Read-only isolation first.",
                success_criteria="Source isolated.",
                rollback_note="Restore subscription if false positive."
            ),
             PlaybookStepRecord(
                step_order=2,
                step_family="quarantine_source",
                rationale="Place source in quarantine for evaluation.",
                safety_bounds="Quarantine limits active.",
                success_criteria="Quarantine active."
            )
        ]
    return [
         PlaybookStepRecord(
                step_order=1,
                step_family="request_manual_review",
                rationale="No automated recovery available.",
                safety_bounds="Review bounded.",
                success_criteria="Review complete."
            )
    ]

def attach_prerequisites_and_risks(playbook: RemediationPlaybookRecord):
    playbook.prerequisites.append(PlaybookPrerequisiteRecord(prerequisite_type="auth", condition="Admin approval", is_met=False))
    playbook.risk_notes.append(PlaybookRiskRecord(risk_level="medium", description="May cause temporary data staleness."))

def attach_validation_and_rollback(playbook: RemediationPlaybookRecord):
     for step in playbook.steps:
         if step.rollback_note:
             playbook.rollback_notes.append(PlaybookRollbackNoteRecord(step_id=str(step.step_order), rollback_action=step.rollback_note))

def synthesize_remediation_playbook(pattern_matches: List[PatternSimilarityRecord], incident_signals: Dict[str, Any]) -> RemediationPlaybookRecord:
    target_family = "generic_incident"
    if pattern_matches and pattern_matches[0].similarity_band in ["strong_match", "plausible_match"]:
        # Naive mapping for demonstration
        target_family = "quarantine_recovery"

    playbook = RemediationPlaybookRecord(
        playbook_id=f"pb_{uuid.uuid4().hex[:8]}",
        playbook_family="standard_recovery",
        target_incident_family=target_family,
        synthesized_from_pattern_refs=[m.pattern_id for m in pattern_matches],
        steps=build_playbook_steps(target_family),
        prerequisites=[],
        risk_notes=[],
        rollback_notes=[],
        expected_signals=["recovery_complete"]
    )
    attach_prerequisites_and_risks(playbook)
    attach_validation_and_rollback(playbook)
    return playbook

def summarize_playbook_quality(playbook: RemediationPlaybookRecord) -> str:
    return f"Playbook {playbook.playbook_id} synthesized with {len(playbook.steps)} steps."
