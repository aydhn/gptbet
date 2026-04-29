from typing import List
import os

class FilesystemAllowlist:
    def __init__(self, allowed_read_roots: List[str] = None, allowed_write_roots: List[str] = None):
        self.allowed_read_roots = allowed_read_roots or ["data/", "configs/", "src/"]
        self.allowed_write_roots = allowed_write_roots or ["data/processed/", "data/artifacts/", "data/cache/", "results/"]

    def validate_read_path(self, path: str) -> bool:
        # In a real impl, resolve paths to absolute and check prefix
        return any(path.startswith(root) for root in self.allowed_read_roots)

    def validate_write_path(self, path: str) -> bool:
        return any(path.startswith(root) for root in self.allowed_write_roots)
