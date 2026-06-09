from sports_signal_bot.verifier_portal.contracts import PortalQueryRecord
from sports_signal_bot.verifier_portal.queries import (
    execute_profile_aware_query, validate_portal_query)


def test_validate_portal_query():
    query1 = PortalQueryRecord(
        query_id="q1", query_type="safe_type", profile="public_viewer"
    )
    safety1 = validate_portal_query(query1)
    assert safety1.safe

    query2 = PortalQueryRecord(
        query_id="q2", query_type="raw_internal", profile="public_viewer"
    )
    safety2 = validate_portal_query(query2)
    assert not safety2.safe


def test_execute_profile_aware_query():
    query = PortalQueryRecord(
        query_id="q1", query_type="safe_type", profile="public_viewer"
    )
    result = execute_profile_aware_query(query)

    assert result.result_id == "res_q1"
    assert result.data["items"][0]["signer_metadata"] == "[REDACTED]"


def test_validate_portal_query_nested_forbidden_keys():
    # Should block nested "key"
    query1 = PortalQueryRecord(
        query_id="q1",
        query_type="safe_type",
        params={"data": {"nested": {"key": "secret"}}},
        profile="public_viewer",
    )
    safety1 = validate_portal_query(query1)
    assert not safety1.safe

    # Should block nested "internal_path" in a list
    query2 = PortalQueryRecord(
        query_id="q2",
        query_type="safe_type",
        params={"data": [{"internal_path": "/etc/passwd"}]},
        profile="public_viewer",
    )
    safety2 = validate_portal_query(query2)
    assert not safety2.safe


def test_validate_portal_query_internal_query_types():
    # Should block case-insensitive "internal"
    query1 = PortalQueryRecord(
        query_id="q1", query_type="RAW_INTERNAL", profile="public_viewer"
    )
    safety1 = validate_portal_query(query1)
    assert not safety1.safe

    query2 = PortalQueryRecord(
        query_id="q2", query_type="some_internal_stuff", profile="public_viewer"
    )
    safety2 = validate_portal_query(query2)
    assert not safety2.safe
