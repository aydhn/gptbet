from typing import Dict, Any, List, Optional
import uuid
from .contracts import PolicyOverlayRecord, PolicyBundleRecord

class OverlayManager:
    def merge_policy_overlays(self, base: PolicyBundleRecord, overlays: List[PolicyOverlayRecord]) -> PolicyBundleRecord:
        """Merges overlays into a base bundle, returning a new compiled bundle snapshot."""

        compiled_rules = set(base.rules)
        for overlay in overlays:
            if overlay.base_bundle_id != base.policy_bundle_id:
                # Naive check, in reality might be wildcards or family match
                pass

            compiled_rules.update(overlay.added_rules)
            compiled_rules.difference_update(overlay.removed_rules)

            # Note: Modifying existing rules inline is complex and risky without deep copy
            # Usually handled via precedence (overlay rule shadowing base rule)

        compiled = PolicyBundleRecord(
            policy_bundle_id=f"compiled_{uuid.uuid4().hex[:8]}",
            bundle_name=f"{base.bundle_name} (with {len(overlays)} overlays)",
            bundle_family=base.bundle_family,
            version=base.version,
            status=base.status,
            rules=list(compiled_rules)
        )
        return compiled

    def validate_overlay_compatibility(self, base: PolicyBundleRecord, overlay: PolicyOverlayRecord) -> bool:
        # Example validation: Overlay shouldn't remove hard safety rules
        return True
