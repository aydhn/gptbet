import uuid
from datetime import datetime
from typing import List

from .contracts import AdjudicationManifest, AdjudicationSummaryRecord


class ManifestBuilder:
    @staticmethod
    def build_manifest(
        summary: AdjudicationSummaryRecord, case_ids: List[str]
    ) -> AdjudicationManifest:
        return AdjudicationManifest(
            manifest_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            version="1.0",
            summary=summary,
            case_ids=case_ids,
        )
