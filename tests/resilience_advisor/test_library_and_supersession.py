from sports_signal_bot.resilience_advisor.library import PlaybookLibrary
from sports_signal_bot.resilience_advisor.contracts import RemediationPlaybookRecord

def test_library_registration():
    library = PlaybookLibrary()
    playbook = RemediationPlaybookRecord(
        playbook_id="pb1", playbook_family="standard_recovery", target_incident_family="sync",
        synthesized_from_pattern_refs=[], steps=[], prerequisites=[],
        risk_notes=[], rollback_notes=[], expected_signals=[]
    )
    library.register_playbook_in_library(playbook)
    assert "Library contains 1 playbooks." in library.summarize_library_health()
    assert len(library.find_candidate_playbooks("sync")) == 1
