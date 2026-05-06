import json
from typing import Dict, Any

def generate_migration_hardening_manifest(summary: Dict[str, Any]) -> str:
    return json.dumps({
        "manifest_version": "1.0",
        "pack": "post_100_hardening_pack_07",
        "summary": summary
    }, indent=2)
