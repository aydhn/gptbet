def check_discovery_health(directory) -> dict:
    return {
        "directory_id": directory.directory_id,
        "catalogs": len(directory.catalogs),
        "health": directory.ecosystem_discovery_health
    }
