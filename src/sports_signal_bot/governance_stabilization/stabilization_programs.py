from .contracts import *

def build_governance_stabilization_program(prog_id: str, family: StabilizationProgramFamily) -> SovereignGovernanceStabilizationProgramRecord:
    return SovereignGovernanceStabilizationProgramRecord(
        stabilization_program_id=prog_id,
        program_family=family
    )

def create_stabilization_checkpoint(program: SovereignGovernanceStabilizationProgramRecord, cp_id: str, family: StabilizationCheckpointFamily):
    cp = StabilizationProgramCheckpointRecord(checkpoint_id=cp_id, family=family)
    program.checkpoints.append(cp)

def advance_stabilization_program(program: SovereignGovernanceStabilizationProgramRecord, target_stage: StabilizationStage):
    # Rule: stabilized state only after explicit checkpoints pass
    if target_stage == StabilizationStage.stabilized:
        if not all(cp.is_cleared for cp in program.checkpoints):
            program.warnings.append("Attempted to advance to 'stabilized' but checkpoints are pending. Blocked.")
            program.current_stage = StabilizationStage.blocked_stabilization
            return
    program.current_stage = target_stage

def verify_stabilization_checkpoints(program: SovereignGovernanceStabilizationProgramRecord, sovereignty_deny_active: bool):
    for cp in program.checkpoints:
        if cp.family == StabilizationCheckpointFamily.sovereignty_constraints_preserved_checkpoint:
            if sovereignty_deny_active:
                cp.is_cleared = False
                program.warnings.append("Sovereignty local deny is active. Checkpoint blocked.")
            else:
                cp.is_cleared = True
