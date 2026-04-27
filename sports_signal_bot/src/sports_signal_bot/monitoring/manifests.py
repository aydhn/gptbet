import json
from pathlib import Path
from sports_signal_bot.monitoring.contracts import MonitoringRunManifest, MonitoringSummaryRecord, HeartbeatRecord

def write_monitoring_manifest(manifest: MonitoringRunManifest, output_dir: str):
    path = Path(output_dir) / "monitoring_manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: f.write(manifest.model_dump_json(indent=2))

def write_heartbeat_record(heartbeat: HeartbeatRecord, output_dir: str):
    path = Path(output_dir) / "heartbeat_record.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: f.write(heartbeat.model_dump_json(indent=2))

def write_monitoring_summary(summary: MonitoringSummaryRecord, output_dir: str):
    path = Path(output_dir) / "global_health_summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: f.write(summary.model_dump_json(indent=2))
