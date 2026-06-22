from typing import Any, Dict


class BaseGeoStrategy:
    def execute_mesh_check(self, mesh: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "ok", "action": "passed"}

    def check_lag(self, lag: int) -> str:
        return "ok"

    def check_asymmetry(self, asymmetry: bool) -> str:
        return "honest"
