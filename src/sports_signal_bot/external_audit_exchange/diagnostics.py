from typing import List, Dict, Any
from .contracts import ExchangeWarningRecord
import uuid

def generate_diagnostics_report(warnings: List[ExchangeWarningRecord]) -> Dict[str, Any]:
    return {
        "total_warnings": len(warnings),
        "warning_types": list(set([w.warning_type for w in warnings]))
    }
