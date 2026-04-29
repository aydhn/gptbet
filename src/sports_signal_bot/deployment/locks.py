import os
import time
from pathlib import Path

def acquire_workspace_lock(state_root: str, operation: str) -> bool:
    lock_file = Path(state_root) / ".workspace.lock"
    if lock_file.exists():
        return False
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_file, "w") as f:
        f.write(f"{operation}:{os.getpid()}:{time.time()}")
    return True

def release_workspace_lock(state_root: str):
    lock_file = Path(state_root) / ".workspace.lock"
    if lock_file.exists():
        lock_file.unlink()

def block_conflicting_operation(state_root: str, operation: str):
    if not acquire_workspace_lock(state_root, operation):
        raise RuntimeError(f"Workspace is locked. Cannot start operation: {operation}")
