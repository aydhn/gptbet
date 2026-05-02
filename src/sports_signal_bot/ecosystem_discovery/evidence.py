def explain_discovery(result) -> str:
    return f"Discovered {len(result.matched_entries)} entries with status: {result.status}"
