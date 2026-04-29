from typing import Optional, Dict, Any
from .contracts import CacheEntryRecord
from datetime import datetime, timezone
import json
import os

class CacheStore:
    def __init__(self, root_dir: str = "data/cache"):
        self.root_dir = root_dir
        os.makedirs(self.root_dir, exist_ok=True)

    def _path(self, family: str, key: str) -> str:
        family_dir = os.path.join(self.root_dir, family)
        os.makedirs(family_dir, exist_ok=True)
        return os.path.join(family_dir, f"{key}.json")

    def get(self, family: str, key: str) -> Optional[Dict[str, Any]]:
        path = self._path(family, key)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            data = json.load(f)
        return data.get("payload")

    def put(self, family: str, key: str, payload: Any, policy: str):
        path = self._path(family, key)
        record = CacheEntryRecord(
            cache_family=family,
            cache_key=key,
            created_at=datetime.now(timezone.utc),
            freshness_policy=policy,
            payload_reference=path,
            last_accessed_at=datetime.now(timezone.utc),
            producer_version="1.0"
        )
        data = {
            "record": record.model_dump(mode='json'),
            "payload": payload
        }
        with open(path, "w") as f:
            json.dump(data, f)
