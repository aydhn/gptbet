from src.sports_signal_bot.final_convergence_hardening import (
    build_production_readiness_review_surface,
    ReviewSurfaceSectionRecord,
    verify_production_readiness_review_surface,
    ReviewSurfaceBlockerRecord
)

def test_review_surface_build_and_verify():
    sections = [ReviewSurfaceSectionRecord(section_id="1", section_type="test")]
    surface = build_production_readiness_review_surface("release_readiness_review_surface", sections)
    assert surface.surface_status == "surface_verified"
    assert verify_production_readiness_review_surface(surface)

def test_hidden_blocker_fails_verification():
    sections = [ReviewSurfaceSectionRecord(section_id="1", section_type="test")]
    surface = build_production_readiness_review_surface("release_readiness_review_surface", sections)
    surface.blocker_refs.append(ReviewSurfaceBlockerRecord(blocker_id="1", hidden=True))
    assert not verify_production_readiness_review_surface(surface)
