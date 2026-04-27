from ..contracts import RefreshAction

def artifact_reresolve_handler(action: RefreshAction) -> bool:
    print(f"Executing RERUN_ARTIFACT_RESOLUTION... parameters: {action.parameters}")
    return True
