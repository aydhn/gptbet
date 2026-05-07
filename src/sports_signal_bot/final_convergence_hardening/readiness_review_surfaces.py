from typing import List, Dict
import uuid
from .contracts import (
    ProductionReadinessReviewSurfaceRecord,
    ReviewSurfaceSectionRecord,
    ReviewSurfaceBlockerRecord,
    ReviewSurfaceResidueRecord,
    ReviewSurfaceGapRecord
)

def build_production_readiness_review_surface(family: str, sections: List[ReviewSurfaceSectionRecord]) -> ProductionReadinessReviewSurfaceRecord:
    return ProductionReadinessReviewSurfaceRecord(
        readiness_review_surface_id=str(uuid.uuid4()),
        surface_family=family, # type: ignore
        section_refs=sections,
        surface_status="surface_verified"
    )

def add_review_surface_section(surface: ProductionReadinessReviewSurfaceRecord, section: ReviewSurfaceSectionRecord):
    surface.section_refs.append(section)

def verify_production_readiness_review_surface(surface: ProductionReadinessReviewSurfaceRecord) -> bool:
    if any(b.hidden for b in surface.blocker_refs):
        return False
    if any(r.hidden for r in surface.residue_refs):
        return False
    if any(g.hidden for g in surface.gap_refs):
        return False
    return True

def summarize_production_readiness_review_surface(surface: ProductionReadinessReviewSurfaceRecord) -> Dict:
    return {
        "id": surface.readiness_review_surface_id,
        "family": surface.surface_family,
        "status": surface.surface_status,
        "sections_count": len(surface.section_refs),
        "blockers_count": len(surface.blocker_refs)
    }
