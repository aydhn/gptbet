import os

dirs = [
    "src/sports_signal_bot/overlay_mesh_governance",
    "src/sports_signal_bot/overlay_mesh_governance/strategies",
    "configs/overlay_mesh_governance",
    "tests/overlay_mesh_governance",
    "docs/operators",
    "docs/reviewers",
    "docs/reference",
    "docs/maintenance"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
