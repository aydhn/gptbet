from typing import Dict, Any

class BaseAlignmentCompilerStrategy:
    """Base class for Alignment Compiler strategies."""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config

    def evaluate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates inputs and returns outcomes."""
        raise NotImplementedError("evaluate() must be implemented by subclass.")
