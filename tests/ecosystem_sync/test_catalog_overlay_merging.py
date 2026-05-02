import pytest
from sports_signal_bot.ecosystem_sync.overlays import OverlayRebuilder
from sports_signal_bot.ecosystem_sync.contracts import OverlayFamily, OverlayMergeOutcome

def test_overlay_build_and_merge():
    rebuilder = OverlayRebuilder(merge_rules={"allow_trust_downgrade": True})
    overlay = rebuilder.build_catalog_overlay("base", OverlayFamily.TRUST, ["source_a"])

    # Merge new entry
    decision = rebuilder.merge_overlay_entries(overlay, [{"ref": "entry_1"}], "source_a")
    assert decision.outcome == OverlayMergeOutcome.CLEAN
    assert "entry_1" in overlay.merged_entry_refs

    # Merge conflicting entry
    decision2 = rebuilder.merge_overlay_entries(overlay, [{"ref": "entry_1"}], "source_b")
    assert decision2.outcome == OverlayMergeOutcome.WITH_CAVEATS
    assert len(decision2.conflicts) == 1
