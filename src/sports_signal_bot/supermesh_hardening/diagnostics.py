def check_stale_support_reuse(has_stale_edge: bool, overrides: bool = False) -> list:
    blockers = []
    if has_stale_edge and not overrides:
        blockers.append("Stale supermesh member accepted as healthy support")
    return blockers

def check_no_safe_visibility(no_safe_preserved: bool) -> list:
    blockers = []
    if not no_safe_preserved:
        blockers.append("No-safe omission under pulse or observatory replay not escalated")
    return blockers

def check_sovereignty_continuity(sovereignty_preserved: bool) -> list:
    blockers = []
    if not sovereignty_preserved:
        blockers.append("Sovereignty visibility loss across boundary not marked critical")
    return blockers
