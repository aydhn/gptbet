import uuid
import hashlib
from typing import List, Dict, Optional

from .contracts import (
    PrecedentRecord,
    AdjudicationCaseRecord
)

class PrecedentRegistry:
    def __init__(self):
        self.precedents: Dict[str, PrecedentRecord] = {}

    def register_precedent(self, record: PrecedentRecord) -> None:
        self.precedents[record.precedent_id] = record

    def get_precedent(self, precedent_id: str) -> Optional[PrecedentRecord]:
        return self.precedents.get(precedent_id)

    def list_precedents(self, active_only: bool = True) -> List[PrecedentRecord]:
        return [p for p in self.precedents.values() if not active_only or p.review_status == "active"]

class PrecedentLookupEngine:
    def __init__(self, registry: PrecedentRegistry):
        self.registry = registry

    def fingerprint_case(self, case: AdjudicationCaseRecord) -> str:
        base = f"{case.case_type.value}|{case.target_entity_type}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]

    def find_matching_precedents(self, case: AdjudicationCaseRecord) -> List[PrecedentRecord]:
        fp = self.fingerprint_case(case)
        matches = []
        for p in self.registry.list_precedents(active_only=True):
            if p.pattern_signature == fp or p.case_family == case.case_type:
                matches.append(p)
        return matches

    def rank_precedent_suggestions(self, case: AdjudicationCaseRecord, matches: List[PrecedentRecord]) -> List[PrecedentRecord]:
        # Sort by usage_count descending as a basic ranking heuristic
        return sorted(matches, key=lambda p: p.usage_count, reverse=True)

    def detect_precedent_conflict(self, case: AdjudicationCaseRecord, matches: List[PrecedentRecord]) -> bool:
        # Simplistic conflict detection: if we have more than 1 match and they have different scopes/constraints
        if len(matches) > 1:
            signatures = set(m.pattern_signature for m in matches)
            return len(signatures) > 1
        return False

    def summarize_precedent_relevance(self, case: AdjudicationCaseRecord, matches: List[PrecedentRecord]) -> str:
        return f"Found {len(matches)} relevant precedents for case type {case.case_type.value}."
