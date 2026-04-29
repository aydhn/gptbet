from typing import Dict, Any, List

class ConfigDoctor:
    def __init__(self, effective_config: Dict[str, Any]):
        self.config = effective_config

    def detect_unknown_keys(self, allowed_keys: List[str]) -> List[str]:
        return [k for k in self.config.keys() if k not in allowed_keys]

    def detect_unsafe_defaults(self) -> List[str]:
        unsafe = []
        if self.config.get("ENABLE_REAL_DISPATCH", False) and self.config.get("SECURITY_PROFILE") == "research_local":
            unsafe.append("ENABLE_REAL_DISPATCH is True in research_local profile")
        return unsafe
