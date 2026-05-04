from .base import BaseProofCatalogStrategy

class ConservativeProofAtlasStrategy(BaseProofCatalogStrategy):
    def __init__(self):
        self.name = "conservative_proof_atlas"
        self.description = "Stale currentness, proof gaps and narrative caveat losses are dominant. Fast caveated/stale."
