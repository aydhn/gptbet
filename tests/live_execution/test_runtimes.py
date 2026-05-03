from sports_signal_bot.live_execution.runtimes import build_runtime_window, init_runtime, execute_step
from sports_signal_bot.live_execution.contracts import RuntimeStepRecord, RuntimeStatus, StepStatus

def test_runtime_execution():
    window = build_runtime_window("2023-01-01", "2023-01-02")
    runtime = init_runtime("lane_1", "tok_1", window)
    step = RuntimeStepRecord(step_ref="s1", step_family="test", planned_order=1)
    assert runtime.runtime_status == RuntimeStatus.READY
    success = execute_step(runtime, step)
    assert success
    assert step.step_status == StepStatus.EXECUTED
