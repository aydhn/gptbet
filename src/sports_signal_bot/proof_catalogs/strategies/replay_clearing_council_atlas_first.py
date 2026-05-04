from .base import BaseProofCatalogStrategy

class ReplayClearingCouncilAtlasFirstStrategy(BaseProofCatalogStrategy):
    def __init__(self):
        self.name = "replay_clearing_council_atlas_first"
        self.description = "Replay evidence, council precedence and proof freshness are dominant."
