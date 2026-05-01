import pytest
from sports_signal_bot.external_audit_exchange.findings import derive_local_actions_from_findings
from sports_signal_bot.external_audit_exchange.contracts import ExternalAuditFindingRecord

def test_derive_local_actions():
    findings = [
        ExternalAuditFindingRecord(finding_id="1", finding_family="test", severity="critical", target_ref="t1", description="desc"),
        ExternalAuditFindingRecord(finding_id="2", finding_family="test", severity="warning", target_ref="t2", description="desc")
    ]
    actions = derive_local_actions_from_findings(findings)
    assert "open_anomaly_case" in actions
    assert "integrity_alert" in actions
    assert "add_supporting_evidence" in actions
