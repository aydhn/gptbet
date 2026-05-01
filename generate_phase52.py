import os
from pathlib import Path

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

ensure_dir("configs/federated_governance")
ensure_dir("src/sports_signal_bot/federated_governance/strategies")
ensure_dir("tests/federated_governance")
ensure_dir("docs/operators")
ensure_dir("docs/reviewers")
ensure_dir("docs/reference")
ensure_dir("docs/maintenance")

print("Directories created.")
