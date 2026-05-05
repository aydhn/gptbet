"""
Determinism logic.
"""
import hashlib
from typing import Dict, Any, List
from .contracts import DeterminismRunRecord

def build_determinism_run(
    run_id: str,
    family: str,
    cmd_ref: str,
    config: Dict[str, Any],
    inputs: Dict[str, Any],
    env: Dict[str, Any],
    seed: str,
    clock: str,
    outputs: Dict[str, str]
) -> DeterminismRunRecord:
    config_str = str(sorted(config.items()))
    input_str = str(sorted(inputs.items()))
    env_str = str(sorted(env.items()))

    return DeterminismRunRecord(
        determinism_run_id=run_id,
        run_family=family,
        source_command_ref=cmd_ref,
        config_hash=hashlib.sha256(config_str.encode()).hexdigest()[:8],
        input_hash=hashlib.sha256(input_str.encode()).hexdigest()[:8],
        environment_hash=hashlib.sha256(env_str.encode()).hexdigest()[:8],
        seed_ref=seed,
        clock_ref=clock,
        output_hashes=outputs,
        parity_status="parity_matched"
    )

def normalize_execution_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in sorted(inputs.items())}

def compare_determinism_runs(run1: DeterminismRunRecord, run2: DeterminismRunRecord) -> str:
    if run1.input_hash == run2.input_hash and run1.config_hash == run2.config_hash and run1.seed_ref == run2.seed_ref:
        if run1.output_hashes != run2.output_hashes:
            return "parity_mismatched"
    return "parity_matched"

def summarize_determinism_parity(runs: List[DeterminismRunRecord]) -> Dict[str, Any]:
    matched = sum(1 for r in runs if r.parity_status == "parity_matched")
    mismatched = sum(1 for r in runs if r.parity_status == "parity_mismatched")
    return {
        "total_runs": len(runs),
        "matched": matched,
        "mismatched": mismatched
    }
