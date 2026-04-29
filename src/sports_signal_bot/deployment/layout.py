import os
from pathlib import Path
from .contracts import DeploymentLayoutRecord

def resolve_workspace_root() -> Path:
    env_path = os.environ.get("SSB_WORKSPACE_ROOT")
    if env_path:
        return Path(env_path).resolve()
    # Repo default relative to this file
    return Path(__file__).resolve().parent.parent.parent.parent

def build_deployment_layout(workspace_root: Path) -> DeploymentLayoutRecord:
    return DeploymentLayoutRecord(
        workspace_root=str(workspace_root),
        config_root=str(workspace_root / "configs"),
        data_root=str(workspace_root / "data"),
        artifacts_root=str(workspace_root / "artifacts"),
        cache_root=str(workspace_root / "cache"),
        logs_root=str(workspace_root / "logs"),
        state_root=str(workspace_root / "state"),
        backups_root=str(workspace_root / "backups"),
        secrets_root=str(workspace_root / "secrets"),
        reports_root=str(workspace_root / "reports"),
        temp_root=str(workspace_root / "temp")
    )

def ensure_layout_exists(layout: DeploymentLayoutRecord, dry_run: bool = False):
    roots = [
        layout.config_root, layout.data_root, layout.artifacts_root,
        layout.cache_root, layout.logs_root, layout.state_root,
        layout.backups_root, layout.secrets_root, layout.reports_root,
        layout.temp_root
    ]
    for r in roots:
        p = Path(r)
        if not p.exists() and not dry_run:
            p.mkdir(parents=True, exist_ok=True)
