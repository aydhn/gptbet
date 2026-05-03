import os
from pathlib import Path

files = [
    "configs/remediation_lanes/lanes.yaml",
    "configs/remediation_lanes/tokens.yaml",
    "configs/remediation_lanes/closure.yaml",
    "configs/remediation_lanes/federated_catalogs.yaml",
    "configs/remediation_lanes/automation_prep.yaml",
]

for f in files:
    Path(f).touch(exist_ok=True)
