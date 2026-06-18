import json
import os
from datetime import datetime, timezone

from .contracts import MaterializationRecord


class LazyManifestLoader:
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path
        self._metadata = None
        self._payload = None

    def load_metadata_only(self):
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, "r") as f:
                data = json.load(f)
                self._metadata = {"id": data.get("id")}
        return self._metadata

    def materialize_payload(self):
        if not self._payload and os.path.exists(self.manifest_path):
            with open(self.manifest_path, "r") as f:
                self._payload = json.load(f)
        return self._payload


class LazyTableReader:
    def __init__(self, table_path: str):
        self.table_path = table_path
        self._columns = None

    def materialize_columns_subset(self, columns: list):
        if not os.path.exists(self.table_path):
            return []
        import csv

        results = []
        with open(self.table_path, "r") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if not fieldnames:
                return []
            columns_set = set(columns)
            valid_cols = tuple(c for c in fieldnames if c in columns_set)
            for row in reader:
                results.append({k: row[k] for k in valid_cols})
        return results


def track_lazy_materialization(handle_id: str) -> MaterializationRecord:
    return MaterializationRecord(
        handle_id=handle_id, materialized_at=datetime.now(timezone.utc)
    )
