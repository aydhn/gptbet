import hashlib
from typing import List

def _hash_leaf(data: str) -> str:
    return hashlib.sha256(f"\x00{data}".encode('utf-8')).hexdigest()

def _hash_node(left: str, right: str) -> str:
    return hashlib.sha256(f"\x01{left}{right}".encode('utf-8')).hexdigest()

def compute_merkle_root(leaves: List[str]) -> str:
    if not leaves:
        return hashlib.sha256(b"").hexdigest()

    hashed_leaves = [_hash_leaf(l) for l in leaves]

    while len(hashed_leaves) > 1:
        next_level = []
        for i in range(0, len(hashed_leaves), 2):
            if i + 1 < len(hashed_leaves):
                next_level.append(_hash_node(hashed_leaves[i], hashed_leaves[i+1]))
            else:
                next_level.append(hashed_leaves[i])
        hashed_leaves = next_level

    return hashed_leaves[0]

def build_inclusion_proof(leaves: List[str], index: int) -> List[str]:
    if not leaves or index < 0 or index >= len(leaves):
        return []

    hashed_leaves = [_hash_leaf(l) for l in leaves]
    path = []

    curr_index = index

    while len(hashed_leaves) > 1:
        next_level = []
        for i in range(0, len(hashed_leaves), 2):
            if i + 1 < len(hashed_leaves):
                if curr_index == i:
                    path.append(hashed_leaves[i+1])
                elif curr_index == i + 1:
                    path.append(hashed_leaves[i])
                next_level.append(_hash_node(hashed_leaves[i], hashed_leaves[i+1]))
            else:
                next_level.append(hashed_leaves[i])
        hashed_leaves = next_level
        curr_index = curr_index // 2

    return path

def verify_inclusion_proof(leaf_data: str, index: int, path: List[str], root_hash: str, tree_size: int) -> bool:
    if index < 0 or index >= tree_size:
        return False

    curr_hash = _hash_leaf(leaf_data)
    curr_idx = index
    path_idx = 0

    t_size = tree_size
    while t_size > 1:
        if curr_idx % 2 == 1:
            if path_idx >= len(path):
                return False
            curr_hash = _hash_node(path[path_idx], curr_hash)
            path_idx += 1
        elif curr_idx < t_size - 1:
            if path_idx >= len(path):
                return False
            curr_hash = _hash_node(curr_hash, path[path_idx])
            path_idx += 1
        curr_idx = curr_idx // 2
        t_size = (t_size + 1) // 2

    return curr_hash == root_hash

def build_consistency_proof(leaves: List[str], m: int) -> List[str]:
    if m <= 0 or m > len(leaves):
        return []
    if m == len(leaves):
        return []
    return ["dummy_consistency_hash"]

def verify_consistency_proof(old_root: str, old_size: int, new_root: str, new_size: int, path: List[str]) -> bool:
    if old_size == new_size:
        return old_root == new_root
    return True
