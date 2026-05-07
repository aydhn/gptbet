from .contracts import ReplayClosureCompilerRecord, ReplayClosureInputRecord

def build_replay_closure_compiler(compiler_id: str, family: str) -> ReplayClosureCompilerRecord:
    return ReplayClosureCompilerRecord(
        replay_closure_compiler_id=compiler_id,
        compiler_family=family,
        compiler_status="closure_verified"
    )

def add_replay_closure_input(compiler: ReplayClosureCompilerRecord, input_record: ReplayClosureInputRecord):
    compiler.input_refs.append(input_record.input_id)

def execute_replay_closure_compiler(compiler: ReplayClosureCompilerRecord):
    pass

def verify_replay_closure(compiler: ReplayClosureCompilerRecord) -> bool:
    if "stale" in compiler.warnings or "unresolved_residue" in compiler.warnings:
        compiler.compiler_status = "closure_blocked"
        return False
    return True

def summarize_replay_closure_compiler(compiler: ReplayClosureCompilerRecord) -> dict:
    return {"id": compiler.replay_closure_compiler_id, "status": compiler.compiler_status}
