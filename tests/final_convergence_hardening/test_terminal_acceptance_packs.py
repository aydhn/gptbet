from src.sports_signal_bot.final_convergence_hardening import (
    build_terminal_acceptance_pack,
    AcceptancePackSectionRecord,
    verify_terminal_acceptance_pack,
    AcceptancePackResidueRecord
)

def test_acceptance_pack_build_and_verify():
    sections = [AcceptancePackSectionRecord(section_id="1", section_type="test")]
    pack = build_terminal_acceptance_pack("final_readiness_acceptance_pack", sections)
    assert pack.pack_status == "pack_verified"
    assert verify_terminal_acceptance_pack(pack)

def test_hidden_residue_fails_verification():
    sections = [AcceptancePackSectionRecord(section_id="1", section_type="test")]
    pack = build_terminal_acceptance_pack("final_readiness_acceptance_pack", sections)
    pack.residue_refs.append(AcceptancePackResidueRecord(residue_id="1", hidden=True))
    assert not verify_terminal_acceptance_pack(pack)
