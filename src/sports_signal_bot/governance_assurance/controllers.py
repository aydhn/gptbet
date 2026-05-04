def enforce_phase90_currentness_caveat_scope_rules(state: str) -> bool:
    if state == "stale":
        return False
    return True

def cap_phase90_outputs_due_to_staleness_or_debt(current_cap: str, is_stale: bool, has_debt: bool) -> str:
    if is_stale or has_debt:
        return "capped_score"
    return current_cap

def enforce_sovereignty_across_phase90(has_sovereignty_failure: bool) -> str:
    if has_sovereignty_failure:
        return "blocked_by_sovereignty"
    return "allowed"
