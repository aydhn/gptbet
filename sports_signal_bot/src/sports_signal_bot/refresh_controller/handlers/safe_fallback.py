from ..contracts import RefreshAction

def safe_fallback_handler(action: RefreshAction) -> bool:
    print(f"Executing ENABLE_SAFE_FALLBACK_MODE... parameters: {action.parameters}")
    return True
