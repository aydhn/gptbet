from datetime import datetime
from typing import Any, Dict, List, Optional


class ProviderSnapshotRecord:
    def __init__(
        self, provider_name: str, data_family: str, payload: Any, fetched_at: datetime
    ):
        self.provider_name = provider_name
        self.data_family = data_family
        self.payload = payload
        self.fetched_at = fetched_at


# Placeholder for snapshot cache interactions
def save_provider_snapshot(snapshot: ProviderSnapshotRecord, path: str):
    pass


def load_provider_snapshot(
    provider_name: str, data_family: str, path: str
) -> Optional[ProviderSnapshotRecord]:
    return None
