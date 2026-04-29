import pytest
from sports_signal_bot.schema_governance.manifests import compute_manifest_hash_placeholder

def test_schema_manifest_hashing():
    payload1 = {"a": 1, "b": 2}
    payload2 = {"b": 2, "a": 1} # Order diff

    h1 = compute_manifest_hash_placeholder(payload1)
    h2 = compute_manifest_hash_placeholder(payload2)

    assert h1 == h2
