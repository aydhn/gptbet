import pytest
from sports_signal_bot.governance_stabilization.contracts import *
from sports_signal_bot.governance_stabilization.controllers import GovernanceStabilizationController
from sports_signal_bot.governance_stabilization.stabilization_programs import build_governance_stabilization_program, create_stabilization_checkpoint

def test_sovereignty_deny_blocks_stabilization():
    ctrl = GovernanceStabilizationController()
    prog = build_governance_stabilization_program("prog_test", StabilizationProgramFamily.quorum_stabilization_program)
    create_stabilization_checkpoint(prog, "cp_sov", StabilizationCheckpointFamily.sovereignty_constraints_preserved_checkpoint)
    ctrl.programs.append(prog)

    # Run with local deny = True
    manifest = ctrl.run_stabilization_pass(local_deny_present=True)

    assert manifest.system_health == "degraded"
    assert manifest.stabilization_programs[0].current_stage == StabilizationStage.blocked_stabilization
    assert "Local sovereignty DENY overrides all stabilization efforts." in manifest.stabilization_programs[0].warnings

def test_lineage_gap_caps_stabilization():
    from sports_signal_bot.governance_stabilization.lineage_registries import build_exception_lineage_registry, register_exception_lineage_entry
    ctrl = GovernanceStabilizationController()

    reg = build_exception_lineage_registry("reg_1", ExceptionLineageRegistryFamily.sovereign_exception_lineage_registry)
    register_exception_lineage_entry(reg, ExceptionLineageEntryRecord(
        lineage_entry_id="e1", exception_ref="ex1", status=ExceptionLineageEntryStatus.lineage_expired
    ))

    ctrl.registries.append(reg)
    ctrl.run_stabilization_pass()

    assert "Lineage gap detected at e1" in ctrl.registries[0].warnings
