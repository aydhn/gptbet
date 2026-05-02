from typing import List, Dict, Any, Optional
from datetime import datetime
from .contracts import (
    CatalogOverlayRecord,
    OverlayMergeDecisionRecord,
    OverlayMergeOutcome,
    OverlayConflictRecord,
    OverlayLineageRecord,
    OverlayFamily
)

class OverlayRebuilder:
    """Handles rebuilding catalog overlays from sources."""
    def __init__(self, merge_rules: Dict[str, Any]):
        self.merge_rules = merge_rules

    def build_catalog_overlay(self, base_ref: str, overlay_family: OverlayFamily, sources: List[str]) -> CatalogOverlayRecord:
        """Builds a new empty catalog overlay."""
        return CatalogOverlayRecord(
            overlay_id=f"overlay_{datetime.utcnow().timestamp()}",
            overlay_family=overlay_family,
            base_catalog_ref=base_ref,
            source_catalog_refs=sources,
            merged_entry_refs=[],
            overlay_policy_ref="default_overlay_policy",
            lineage_refs=[],
            freshness_state="fresh",
            trust_state="trusted",
            warnings=[]
        )

    def merge_overlay_entries(self, overlay: CatalogOverlayRecord, new_entries: List[Dict[str, Any]], source_ref: str) -> OverlayMergeDecisionRecord:
        """Merges new entries into the overlay, detecting conflicts."""
        conflicts = self.detect_overlay_conflicts(overlay, new_entries)

        outcome = OverlayMergeOutcome.CLEAN
        if conflicts:
            outcome = self.resolve_overlay_conflicts(conflicts)

        # In a real system, we'd merge the actual data structure.
        # Here we just track the refs and lineage.
        for entry in new_entries:
            entry_ref = entry.get("ref")
            if entry_ref and entry_ref not in overlay.merged_entry_refs:
                overlay.merged_entry_refs.append(entry_ref)
                self.preserve_overlay_lineage(overlay, entry_ref, source_ref, "hash_placeholder")

        if outcome == OverlayMergeOutcome.QUARANTINED:
            overlay.trust_state = "quarantined"

        return OverlayMergeDecisionRecord(
            decision_id=f"decision_{datetime.utcnow().timestamp()}",
            overlay_id=overlay.overlay_id,
            outcome=outcome,
            conflicts=conflicts
        )

    def preserve_overlay_lineage(self, overlay: CatalogOverlayRecord, entry_ref: str, source_ref: str, provenance_hash: str) -> None:
        """Preserves the lineage of an entry in the overlay."""
        overlay.lineage_refs.append(
            OverlayLineageRecord(
                source_ref=source_ref,
                provenance_hash=provenance_hash,
                timestamp=datetime.utcnow()
            )
        )

    def rebuild_overlay_from_sources(self, overlay: CatalogOverlayRecord, source_data_maps: Dict[str, List[Dict[str, Any]]]) -> OverlayMergeDecisionRecord:
        """Completely rebuilds an overlay from a fresh set of source data."""
        overlay.merged_entry_refs = []
        overlay.lineage_refs = []

        all_conflicts = []
        worst_outcome = OverlayMergeOutcome.CLEAN

        for source_ref, entries in source_data_maps.items():
            decision = self.merge_overlay_entries(overlay, entries, source_ref)
            all_conflicts.extend(decision.conflicts)

            # Very simplistic worst-outcome logic
            if decision.outcome == OverlayMergeOutcome.QUARANTINED:
                worst_outcome = OverlayMergeOutcome.QUARANTINED
            elif decision.outcome == OverlayMergeOutcome.WITH_CAVEATS and worst_outcome == OverlayMergeOutcome.CLEAN:
                worst_outcome = OverlayMergeOutcome.WITH_CAVEATS

        return OverlayMergeDecisionRecord(
            decision_id=f"decision_rebuild_{datetime.utcnow().timestamp()}",
            overlay_id=overlay.overlay_id,
            outcome=worst_outcome,
            conflicts=all_conflicts
        )

    def summarize_overlay_state(self, overlay: CatalogOverlayRecord) -> Dict[str, Any]:
        """Summarizes the current state of an overlay."""
        return {
            "overlay_id": overlay.overlay_id,
            "entry_count": len(overlay.merged_entry_refs),
            "source_count": len(overlay.source_catalog_refs),
            "freshness": overlay.freshness_state,
            "trust": overlay.trust_state
        }

    def detect_overlay_conflicts(self, overlay: CatalogOverlayRecord, new_entries: List[Dict[str, Any]]) -> List[OverlayConflictRecord]:
        """Detects conflicts between existing overlay entries and new ones."""
        conflicts = []
        # Mock conflict detection based on existing refs
        for entry in new_entries:
            ref = entry.get("ref")
            if ref in overlay.merged_entry_refs:
                # Mock a trust conflict if it already exists
                conflicts.append(OverlayConflictRecord(
                    conflict_type="trust_conflict",
                    refs=[ref],
                    description="Entry already exists with potentially different trust level."
                ))
        return conflicts

    def resolve_overlay_conflicts(self, conflicts: List[OverlayConflictRecord]) -> OverlayMergeOutcome:
        """Resolves conflicts based on rules, returning the overall outcome."""
        if not conflicts:
            return OverlayMergeOutcome.CLEAN

        for conflict in conflicts:
            if conflict.conflict_type == "availability_conflict":
                return OverlayMergeOutcome.QUARANTINED
            elif conflict.conflict_type == "trust_conflict" and not self.merge_rules.get("allow_trust_downgrade", True):
                return OverlayMergeOutcome.CONFLICT_RETAINED

        return OverlayMergeOutcome.WITH_CAVEATS

    def retain_conflict_for_review(self, conflict: OverlayConflictRecord) -> None:
        """Marks a conflict to be retained for human review."""
        pass

    def mark_overlay_entry_current_or_not(self, entry_ref: str, is_current: bool) -> None:
        """Marks an entry as current or stale."""
        pass
