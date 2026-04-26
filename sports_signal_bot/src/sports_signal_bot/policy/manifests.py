import json
from pathlib import Path
from sports_signal_bot.policy.contracts import PolicyManifest

def export_policy_manifest(manifest: PolicyManifest, output_dir: str):
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)

    with open(path / "policy_manifest.json", "w") as f:
        f.write(manifest.model_dump_json(indent=2))

    with open(path / "policy_decisions.json", "w") as f:
        decisions = [d.model_dump(mode="json") for d in manifest.decisions]
        json.dump(decisions, f, indent=2)

    with open(path / "policy_lifecycle.json", "w") as f:
        lifecycles = [lc.model_dump(mode="json") for lc in manifest.lifecycle_events]
        json.dump(lifecycles, f, indent=2)
