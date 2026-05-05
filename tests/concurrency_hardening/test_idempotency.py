import pytest
from sports_signal_bot.concurrency_hardening.idempotency import build_idempotency_contract, build_idempotency_key, detect_duplicate_execution

def test_build_idempotency_contract():
    contract = build_idempotency_contract("target_1", "key_1")
    assert contract.target_ref == "target_1"
    assert contract.status == "protected"

def test_build_idempotency_key():
    key = build_idempotency_key("some_data")
    assert len(key.value) > 0

def test_detect_duplicate_execution():
    assert detect_duplicate_execution(["key_1", "key_2"], "key_1") == True
    assert detect_duplicate_execution(["key_1", "key_2"], "key_3") == False
