import sys
from pathlib import Path
from .contracts import EnvironmentDoctorRecord, DoctorCheckRecord, DoctorSeverity, DeploymentLayoutRecord

def run_environment_doctor(layout: DeploymentLayoutRecord) -> EnvironmentDoctorRecord:
    checks = []

    # 1. Python runtime
    py_version = sys.version_info
    if py_version.major == 3 and py_version.minor >= 11:
        checks.append(DoctorCheckRecord(
            family="python_runtime", name="Version Check",
            severity=DoctorSeverity.OK, message=f"Python version {py_version.major}.{py_version.minor} is supported."
        ))
    else:
        checks.append(DoctorCheckRecord(
            family="python_runtime", name="Version Check",
            severity=DoctorSeverity.CRITICAL, message="Python 3.11+ is required.",
            blocking=True
        ))

    # 2. Workspace Layout Check
    missing_dirs = []
    roots = [layout.config_root, layout.data_root, layout.secrets_root]
    for r in roots:
        if not Path(r).exists():
            missing_dirs.append(r)

    if missing_dirs:
        checks.append(DoctorCheckRecord(
            family="workspace_layout", name="Directory Presence",
            severity=DoctorSeverity.WARNING, message=f"Missing directories: {missing_dirs}",
            remediation="Run `python -m sports_signal_bot.main bootstrap`"
        ))
    else:
        checks.append(DoctorCheckRecord(
            family="workspace_layout", name="Directory Presence",
            severity=DoctorSeverity.OK, message="All required roots exist."
        ))

    # Summarize
    counts = {s: 0 for s in DoctorSeverity}
    for c in checks:
        counts[c.severity] += 1

    is_ready = counts[DoctorSeverity.CRITICAL] == 0
    return EnvironmentDoctorRecord(checks=checks, is_ready=is_ready, summary_counts=counts)
