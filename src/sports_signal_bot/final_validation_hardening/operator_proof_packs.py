from .contracts import OperatorProofPackRecord, ProofPackSectionRecord

def build_operator_proof_pack(pack_id: str, family: str) -> OperatorProofPackRecord:
    return OperatorProofPackRecord(
        operator_proof_pack_id=pack_id,
        pack_family=family,
        pack_status="pack_verified"
    )

def add_proof_pack_section(pack: OperatorProofPackRecord, section: ProofPackSectionRecord):
    pack.section_refs.append(section.section_id)

def verify_operator_proof_pack(pack: OperatorProofPackRecord) -> bool:
    if "stale" in pack.warnings:
        pack.pack_status = "pack_blocked"
        return False
    return True

def replay_operator_proof_pack(pack: OperatorProofPackRecord):
    pass

def summarize_operator_proof_pack(pack: OperatorProofPackRecord) -> dict:
    return {"id": pack.operator_proof_pack_id, "status": pack.pack_status}
