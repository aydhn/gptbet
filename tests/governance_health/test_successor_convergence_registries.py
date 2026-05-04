import pytest
from sports_signal_bot.governance_health import (
    build_successor_convergence_registry,
    register_convergence_entry,
    compute_convergence_band,
    summarize_convergence_registry
)

def test_registry_creation():
    registry = build_successor_convergence_registry("sovereign_successor_convergence_registry")
    assert registry.registry_family == "sovereign_successor_convergence_registry"

def test_entry_registration_and_band():
    registry = build_successor_convergence_registry("sovereign_successor_convergence_registry")
    entry = register_convergence_entry(registry, "source_ref", ["cand1", "cand2"])

    assert len(registry.entry_refs) == 1
    assert "source_ref" in registry.tracked_successor_refs

    band = compute_convergence_band(entry, "low", "matched", False)
    assert band == "bounded_convergence"

    band = compute_convergence_band(entry, "high", "mismatched", False)
    assert band == "no_convergence"

    band = compute_convergence_band(entry, "high", "matched", True)
    assert band == "stale_convergence"

def test_registry_summary():
    registry = build_successor_convergence_registry("sovereign_successor_convergence_registry")
    entry = register_convergence_entry(registry, "source_ref", ["cand1"])
    compute_convergence_band(entry, "low", "matched", False) # bounded

    summary = summarize_convergence_registry(registry, [entry])
    assert summary["health_status"] == "stable"
    assert summary["band_distribution"]["bounded_convergence"] == 1
