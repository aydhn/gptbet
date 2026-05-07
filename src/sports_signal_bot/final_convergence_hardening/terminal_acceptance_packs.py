from typing import List, Dict
import uuid
from .contracts import (
    TerminalAcceptancePackRecord,
    AcceptancePackSectionRecord,
    AcceptancePackEvidenceRecord,
    AcceptancePackReplayRecord
)

def build_terminal_acceptance_pack(family: str, sections: List[AcceptancePackSectionRecord]) -> TerminalAcceptancePackRecord:
    return TerminalAcceptancePackRecord(
        terminal_acceptance_pack_id=str(uuid.uuid4()),
        pack_family=family, # type: ignore
        section_refs=sections,
        pack_status="pack_verified"
    )

def add_acceptance_pack_section(pack: TerminalAcceptancePackRecord, section: AcceptancePackSectionRecord):
    pack.section_refs.append(section)

def verify_terminal_acceptance_pack(pack: TerminalAcceptancePackRecord) -> bool:
    if any(b.hidden for b in pack.blocker_refs):
        return False
    if any(r.hidden for r in pack.residue_refs):
        return False
    if any(g.hidden for g in pack.gap_refs):
        return False
    return True

def replay_terminal_acceptance_pack(pack: TerminalAcceptancePackRecord) -> bool:
    if not pack.evidence_refs:
        return False
    return all(e.replayable for e in pack.evidence_refs)

def summarize_terminal_acceptance_pack(pack: TerminalAcceptancePackRecord) -> Dict:
    return {
        "id": pack.terminal_acceptance_pack_id,
        "family": pack.pack_family,
        "status": pack.pack_status,
        "sections_count": len(pack.section_refs),
        "evidence_count": len(pack.evidence_refs)
    }
