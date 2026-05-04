from typing import Dict, Any

class BaseOverlayMeshStrategy:
    def __init__(self, name: str):
        self.name = name

    def execute(self) -> Dict[str, Any]:
        return {"strategy": self.name, "status": "executed"}
