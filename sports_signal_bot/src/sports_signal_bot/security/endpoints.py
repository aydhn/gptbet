from typing import List

class EndpointAllowlist:
    def __init__(self, allowed_endpoints: List[str] = None):
        self.allowed_endpoints = allowed_endpoints or ["api.telegram.org"]

    def validate_outbound_endpoint(self, endpoint: str) -> bool:
        return any(allowed in endpoint for allowed in self.allowed_endpoints)
