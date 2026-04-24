import random
import numpy as np

_GLOBAL_SEED = None

def set_global_seed(seed: int = 42) -> None:
    """Sets seed for standard library and numpy for reproducibility."""
    global _GLOBAL_SEED
    _GLOBAL_SEED = seed
    random.seed(seed)
    np.random.seed(seed)

def get_global_seed() -> int:
    return _GLOBAL_SEED
