import typer
import json
import os
import datetime
from ..live_execution.engines import build_execution_engine
from ..live_execution.runtimes import build_runtime_window, init_runtime, execute_step
from ..live_execution.contracts import RuntimeStepRecord, LiveExecutionManifest
from ..live_execution.renewals import request_renewal, decide_renewal
from ..live_execution.rollback_automata import build_lane_rollback_automaton, arm_rollback_automaton
from ..live_execution.closure import start_closure_verification_session

app = typer.Typer(help="Live Execution commands")

@app.command()
def run_live_execution_pass():
    typer.echo("Running live execution pass...")
    engine = build_execution_engine("eng_1", "bounded_lane_execution_engine")
    window = build_runtime_window("2023-01-01T00:00:00Z", "2023-01-01T01:00:00Z")
    runtime = init_runtime("lane_replay_1", "tok_valid_1", window)
    step1 = RuntimeStepRecord(step_ref="step_1", step_family="reduce_replay_backlog_step", planned_order=1)
    execute_step(runtime, step1)

    renewal = request_renewal("lane_degraded_2", "tok_expiring_2")
    renewal = decide_renewal(renewal, approve=True, tighter_scope=True)

    automaton = build_lane_rollback_automaton("lane_sync_3")
    automaton = arm_rollback_automaton(automaton)

    closure = start_closure_verification_session("lane_replay_1", ["checkpoint_sequence_completed"])

    manifest = LiveExecutionManifest(
        manifest_id="live_manifest_001",
        timestamp=datetime.datetime.now().isoformat(),
        runtimes=[runtime],
        renewals=[renewal],
        rollback_automata=[automaton],
        closure_controllers=[closure],
        summary={
            "live_capable_lane_count": 4,
            "runtime_entered": 1,
            "token_renewals_approved": 1,
            "rollback_automata_armed": 1,
            "closure_sessions_pending": 1
        }
    )

    os.makedirs("results", exist_ok=True)
    with open("results/live_execution_manifest.json", "w") as f:
        f.write(manifest.model_dump_json(indent=2))

    typer.echo(f"Manifest written to results/live_execution_manifest.json")
    typer.echo(f"Summary: {json.dumps(manifest.summary, indent=2)}")

@app.command()
def list_live_execution_strategies():
    typer.echo("Live Execution Strategies:")
    typer.echo("- ConservativeLiveLaneStrategy")
    typer.echo("- BalancedSupervisedRuntimeStrategy")
    typer.echo("- FederatedRuntimeAwareStrategy")
    typer.echo("- ClosureDominantStrategy")
    typer.echo("- RenewalStrictStrategy")

if __name__ == "__main__":
    app()
