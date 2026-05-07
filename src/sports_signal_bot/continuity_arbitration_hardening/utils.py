from typing import Dict, Any

def extract_release_blockers(report: Dict[str, Any]) -> list:
    from .diagnostics import check_release_blockers
    return check_release_blockers(report)
