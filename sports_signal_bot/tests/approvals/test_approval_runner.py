from sports_signal_bot.approvals.runner import ApprovalRunner
from sports_signal_bot.approvals.registry import ApprovalRegistry
from sports_signal_bot.approvals.requests import ApprovalRequestBuilder
from sports_signal_bot.approvals.contracts import RequestType, ApprovalScope, OperatorIdentityRecord
import tempfile

def test_approval_runner_process():
    with tempfile.TemporaryDirectory() as tmp:
        registry = ApprovalRegistry(tmp)
        runner = ApprovalRunner(registry)

        req = ApprovalRequestBuilder.build_request(
            request_type=RequestType.approve_high_risk_decision,
            request_scope=ApprovalScope.single_event,
            target_entity_type="bet",
            target_entity_id="bet123",
            severity="high",
            origin_component="tests",
            requested_action="dispatch",
            rationale_summary="High risk bet"
        )
        op = OperatorIdentityRecord(operator_id="senior1", display_name="S", role="senior_operator")

        decision = runner.process_decision(req, op, "approve", "Looks good")
        assert decision.execution_authorized is True
        assert req.status == "approved"
