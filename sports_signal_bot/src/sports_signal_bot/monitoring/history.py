import json
from pathlib import Path
from typing import List
from sports_signal_bot.monitoring.contracts import HealthAlertRecord, MonitoringRunManifest

class HealthHistoryStore:
    def __init__(self, history_dir: str):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
    def save_run(self, manifest: MonitoringRunManifest):
        path = self.history_dir / f"{manifest.run_id}.json"
        with open(path, "w") as f: f.write(manifest.model_dump_json(indent=2))
    def load_recent_runs(self, limit: int = 5) -> List[MonitoringRunManifest]:
        files = sorted(self.history_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        runs = []
        for file in files[:limit]:
            try:
                with open(file, "r") as f: runs.append(MonitoringRunManifest.model_validate_json(f.read()))
            except Exception: continue
        return runs

class MonitoringStateTracker:
    def __init__(self, history_store: HealthHistoryStore):
        self.store = history_store
    def get_last_run_alerts(self) -> List[HealthAlertRecord]:
        return []

class ConsecutiveIssueTracker:
    def __init__(self, state_tracker: MonitoringStateTracker):
        self.state_tracker = state_tracker
    def track(self, current_alerts: List[HealthAlertRecord]) -> List[HealthAlertRecord]:
        from sports_signal_bot.monitoring.escalation import track_repeated_failures
        return track_repeated_failures(current_alerts, [self.state_tracker.get_last_run_alerts()])
