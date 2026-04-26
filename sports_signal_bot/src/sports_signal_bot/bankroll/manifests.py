import json
import os
from sports_signal_bot.bankroll.contracts import BankrollRunManifest

def export_bankroll_manifest(manifest: BankrollRunManifest, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    manifest_path = os.path.join(output_dir, f"bankroll_manifest_{manifest.run_id}.json")
    with open(manifest_path, 'w') as f:
        f.write(manifest.model_dump_json(indent=2))
    return manifest_path
