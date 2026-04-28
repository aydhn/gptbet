from typing import Dict, Optional, List
from sports_signal_bot.approvals.contracts import OperatorIdentityRecord, ApprovalScope

class OperatorRegistry:
    def __init__(self):
        self._operators: Dict[str, OperatorIdentityRecord] = {}

    def register_operator(self, operator: OperatorIdentityRecord) -> None:
        self._operators[operator.operator_id] = operator

    def get_operator(self, operator_id: str) -> Optional[OperatorIdentityRecord]:
        return self._operators.get(operator_id)

    def list_operators(self) -> List[OperatorIdentityRecord]:
        return list(self._operators.values())

# Global registry instance
registry = OperatorRegistry()

def load_operators_from_config(config_data: dict) -> None:
    """Load operators from configuration dict."""
    registry._operators.clear()
    for op_id, data in config_data.items():
        op = OperatorIdentityRecord(
            operator_id=op_id,
            display_name=data.get("display_name", op_id),
            role=data.get("role", "operator"),
            active=data.get("active", True),
            approval_scopes=[ApprovalScope(s) for s in data.get("approval_scopes", [])],
            note=data.get("note")
        )
        registry.register_operator(op)
