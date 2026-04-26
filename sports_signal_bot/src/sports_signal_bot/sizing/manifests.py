import json
from sports_signal_bot.sizing.contracts import SizingManifest


def save_sizing_manifest(manifest: SizingManifest, filepath: str):
    """Serialize and save the SizingManifest."""

    # Convert to dict, handling datetime serialization
    def default_serializer(obj):
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        if hasattr(obj, "dict"):
            return obj.dict()
        raise TypeError(f"Type not serializable: {type(obj)}")

    with open(filepath, "w") as f:
        json.dump(manifest.dict(), f, default=default_serializer, indent=2)


def load_sizing_manifest(filepath: str) -> SizingManifest:
    """Load a SizingManifest from file."""
    with open(filepath, "r") as f:
        data = json.load(f)
    return SizingManifest(**data)
