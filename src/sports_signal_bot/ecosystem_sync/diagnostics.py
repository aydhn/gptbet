from typing import List, Dict, Any
from .contracts import SyncWarningRecord

def collect_diagnostics(warnings: List[SyncWarningRecord]) -> Dict[str, Any]:
    """Collects and summarizes diagnostic warnings."""
    return {
        "warning_count": len(warnings),
        "recent_warnings": [w.message for w in warnings[-5:]]
    }
