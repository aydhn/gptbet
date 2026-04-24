import random
import numpy as np

def set_global_seed(seed: int = 42) -> None:
    """Sets seed for standard library and numpy for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
