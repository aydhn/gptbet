import json
from pathlib import Path
from sports_signal_bot.quality.contracts import TestRunManifest, GateExecutionRecord

class TestReporter:
    def __init__(self, output_dir: str = "sports_signal_bot/results/quality"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_run_manifest(self, manifest: TestRunManifest):
        path = self.output_dir / f"quality_manifest_{manifest.run_id}.json"
        with open(path, "w") as f:
            f.write(manifest.model_dump_json(indent=2))

    def write_gate_result(self, execution: GateExecutionRecord):
        path = self.output_dir / f"gate_result_{execution.execution_id}.json"
        with open(path, "w") as f:
            f.write(execution.model_dump_json(indent=2))

    def print_summary(self, manifest: TestRunManifest):
        print(f"Test Run Summary: {manifest.run_id}")
        print(f"Total: {manifest.total_tests}, Passed: {manifest.passed}, Failed: {manifest.failed}")
