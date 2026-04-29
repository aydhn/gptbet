import json
from pathlib import Path
from .contracts import BootstrapMode, DeploymentLayoutRecord
from .layout import build_deployment_layout, ensure_layout_exists
from .profiles import get_install_profile

def run_bootstrap(workspace_root: Path, profile_name: str, mode: BootstrapMode, dry_run: bool = False):
    layout = build_deployment_layout(workspace_root)
    profile = get_install_profile(profile_name)

    plan = {
        "mode": mode.value,
        "profile": profile.name,
        "workspace_root": layout.workspace_root,
        "actions": []
    }

    plan["actions"].append("Ensure deployment layout exists.")
    ensure_layout_exists(layout, dry_run)

    # Generate templates
    env_example = Path(layout.workspace_root) / ".env.local.example"
    if not env_example.exists() and not dry_run:
        env_example.write_text("# SSB Local Env Template\nSSB_ENVIRONMENT=local\n")
    plan["actions"].append(f"Create template {env_example.name}")

    # Save manifest
    manifest_path = Path(layout.artifacts_root) / "bootstrap_manifest.json"
    if not dry_run and Path(layout.artifacts_root).exists():
        manifest_path.write_text(json.dumps(plan, indent=2))

    return plan
