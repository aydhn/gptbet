from sports_signal_bot.approvals.identities import OperatorRegistry
from sports_signal_bot.approvals.contracts import OperatorIdentityRecord

def test_operator_registry():
    registry = OperatorRegistry()
    registry.register_operator(OperatorIdentityRecord(operator_id="op1", display_name="O", role="operator"))

    assert registry.get_operator("op1") is not None
    assert registry.get_operator("unknown") is None
