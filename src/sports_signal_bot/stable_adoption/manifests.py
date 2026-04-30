from typing import List, Dict, Any
import datetime
from .contracts import AdoptionManifest, StableAdoptionRecord, AdoptionSummaryRecord

def build_adoption_manifest(adoptions: List[StableAdoptionRecord], summary: AdoptionSummaryRecord) -> AdoptionManifest:
    return AdoptionManifest(
        manifest_id=f"man_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoptions=adoptions,
        summary=summary
    )
