from sports_signal_bot.verifier_portal.queries import validate_portal_query, execute_profile_aware_query
from sports_signal_bot.verifier_portal.contracts import PortalQueryRecord

def test_validate_portal_query():
    query1 = PortalQueryRecord(query_id="q1", query_type="safe_type", profile="public_viewer")
    safety1 = validate_portal_query(query1)
    assert safety1.safe

    query2 = PortalQueryRecord(query_id="q2", query_type="raw_internal", profile="public_viewer")
    safety2 = validate_portal_query(query2)
    assert not safety2.safe

def test_execute_profile_aware_query():
    query = PortalQueryRecord(query_id="q1", query_type="safe_type", profile="public_viewer")
    result = execute_profile_aware_query(query)

    assert result.result_id == "res_q1"
    assert result.data["items"][0]["signer_metadata"] == "[REDACTED]"
