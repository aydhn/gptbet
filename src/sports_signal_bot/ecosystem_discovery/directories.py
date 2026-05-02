import uuid
from sports_signal_bot.ecosystem_discovery.contracts import (
    EcosystemDirectoryRecord,
    DirectoryNodeRecord,
    DirectoryLinkRecord
)

def build_ecosystem_directory() -> EcosystemDirectoryRecord:
    return EcosystemDirectoryRecord(
        directory_id=f"dir_{uuid.uuid4().hex[:8]}"
    )

def register_directory_node(directory: EcosystemDirectoryRecord, node_type: str, name: str) -> EcosystemDirectoryRecord:
    node = DirectoryNodeRecord(node_id=f"node_{uuid.uuid4().hex[:8]}", node_type=node_type, name=name)
    if node_type == "catalog":
        directory.catalogs.append(node)
    elif node_type == "registry":
        directory.registries.append(node)
    elif node_type == "verifier":
        directory.verifier_nodes.append(node)
    return directory

def connect_directory_links(source_id: str, target_id: str, relationship: str) -> DirectoryLinkRecord:
    return DirectoryLinkRecord(source_id=source_id, target_id=target_id, relationship=relationship)

def summarize_directory_topology(directory: EcosystemDirectoryRecord) -> dict:
    return {
        "directory_id": directory.directory_id,
        "catalogs_count": len(directory.catalogs),
        "registries_count": len(directory.registries),
        "verifiers_count": len(directory.verifier_nodes),
        "health": directory.ecosystem_discovery_health
    }
