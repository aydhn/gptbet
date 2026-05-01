from typing import List
from .contracts import TransparencyAnomalyRecord, AnomalyAdjudicationRecord, AnomalyAdjudicationOutcome
import datetime

class AdjudicationEngine:
    def adjudicate_transparency_anomaly(self, anomaly: TransparencyAnomalyRecord, decision: AnomalyAdjudicationOutcome, rationale: str) -> AnomalyAdjudicationRecord:
        return AnomalyAdjudicationRecord(
            adjudication_id=f"adj_{datetime.datetime.utcnow().timestamp()}",
            anomaly_id=anomaly.anomaly_id,
            outcome=decision,
            rationale=rationale,
            created_at=datetime.datetime.utcnow()
        )
