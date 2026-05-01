import pytest
from sports_signal_bot.transparency.merkle import compute_merkle_root, build_inclusion_proof, verify_inclusion_proof

def test_merkle_tree():
    leaves = ["a", "b", "c", "d", "e"]
    root = compute_merkle_root(leaves)
    assert root is not None

    path = build_inclusion_proof(leaves, 2)
    assert len(path) > 0

    # Test basic validation
    is_valid = verify_inclusion_proof("c", 2, path, root, len(leaves))
    assert is_valid == True

    # Bad verify
    is_invalid = verify_inclusion_proof("wrong", 2, path, root, len(leaves))
    assert is_invalid == False
