from .contracts import InstallProfileRecord

# In a real implementation, this would load from configs/deployment/install_profiles.yaml
def get_install_profile(name: str) -> InstallProfileRecord:
    profiles = {
        "research_local": InstallProfileRecord(
            name="research_local",
            description="Broadest feature set, dry-run friendly, real dispatch off.",
            required_directories=["data", "models", "artifacts"],
            allowed_commands=["bootstrap", "doctor", "backup", "restore"]
        ),
        "conservative_ops": InstallProfileRecord(
            name="conservative_ops",
            description="Stricter secrets checks, stable safe defaults.",
            required_directories=["data", "secrets", "state"],
            allowed_commands=["doctor", "backup", "restore"],
            backup_default_excludes=["cache", "temp"]
        )
    }
    return profiles.get(name, profiles["research_local"])
