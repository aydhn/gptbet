from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DoctorSeverity(str, Enum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class BootstrapMode(str, Enum):
    INIT_NEW_WORKSPACE = "init_new_workspace"
    INIT_REPO_DEFAULT_WORKSPACE = "init_repo_default_workspace"
    REPAIR_MISSING_LAYOUT = "repair_missing_layout"
    DRY_RUN_PREVIEW = "dry_run_preview"

class BackupType(str, Enum):
    METADATA_ONLY_BACKUP = "metadata_only_backup"
    CONFIG_AND_STATE_BACKUP = "config_and_state_backup"
    FULL_LOCAL_BUNDLE_BACKUP = "full_local_bundle_backup"
    PORTABLE_WORKSPACE_BACKUP = "portable_workspace_backup"
    RELEASE_STATE_BACKUP = "release_state_backup"

class DeploymentLayoutRecord(BaseModel):
    workspace_root: str
    config_root: str
    data_root: str
    artifacts_root: str
    cache_root: str
    logs_root: str
    state_root: str
    backups_root: str
    secrets_root: str
    reports_root: str
    temp_root: str
    layout_version: str = "1.0.0"
    warnings: List[str] = Field(default_factory=list)

class InstallProfileRecord(BaseModel):
    name: str
    description: str
    required_directories: List[str] = Field(default_factory=list)
    required_configs: List[str] = Field(default_factory=list)
    allowed_commands: List[str] = Field(default_factory=list)
    backup_default_excludes: List[str] = Field(default_factory=list)

class DoctorCheckRecord(BaseModel):
    family: str
    name: str
    severity: DoctorSeverity
    message: str
    remediation: Optional[str] = None
    blocking: bool = False

class EnvironmentDoctorRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    checks: List[DoctorCheckRecord] = Field(default_factory=list)
    is_ready: bool = False
    summary_counts: Dict[DoctorSeverity, int] = Field(default_factory=dict)

class BackupManifestRecord(BaseModel):
    backup_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    backup_type: BackupType
    included_families: List[str] = Field(default_factory=list)
    excluded_families: List[str] = Field(default_factory=list)
    size_bytes: int = 0
    redaction_mode: str = "redacted"
    layout_version: str = "1.0.0"

class MigrationPreflightRecord(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    current_layout_version: str
    current_schema_version: str
    required_migrations: List[str] = Field(default_factory=list)
    blocking_issues: List[str] = Field(default_factory=list)
    backup_recommended: bool = True
