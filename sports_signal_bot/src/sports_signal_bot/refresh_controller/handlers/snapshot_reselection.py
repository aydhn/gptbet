from ..contracts import RefreshAction

def snapshot_reselection_handler(action: RefreshAction) -> bool:
    print(f"Executing SNAPSHOT_RESELECTION... parameters: {action.parameters}")
    return True
