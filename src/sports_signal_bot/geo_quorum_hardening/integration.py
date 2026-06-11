import json
import os
from typing import Any, Dict, Tuple

from src.sports_signal_bot.geo_quorum_hardening.strategies import (
    BalancedGeoQuorumReadinessStrategy,
    BaseGeoQuorumHardeningStrategy,
    ConservativeGeoQuorumHardeningStrategy,
    QuorumIntegrityFirstStrategy,
)


def get_strategy(name: str) -> BaseGeoQuorumHardeningStrategy:
    strategies = {
        "conservative": ConservativeGeoQuorumHardeningStrategy(),
        "balanced": BalancedGeoQuorumReadinessStrategy(),
        "quorum_integrity_first": QuorumIntegrityFirstStrategy(),
    }
    return strategies.get(name, ConservativeGeoQuorumHardeningStrategy())


def save_artifact(filename: str, data: Any):
    os.makedirs("out/geo_quorum_hardening", exist_ok=True)
    filepath = os.path.join("out/geo_quorum_hardening", filename)
    with open(filepath, "w") as f:
        if isinstance(data, list):
            dump_data = [
                item.model_dump() if hasattr(item, "model_dump") else item
                for item in data
            ]
            json.dump(dump_data, f, indent=2, default=str)
        elif hasattr(data, "model_dump"):
            json.dump(data.model_dump(), f, indent=2, default=str)
        else:
            json.dump(data, f, indent=2, default=str)


def _execute_core_hardening_processes() -> Tuple[Any, Any, Any, Any]:
    from src.sports_signal_bot.geo_quorum_hardening.active_passive import (
        build_active_passive_rehearsal,
    )
    from src.sports_signal_bot.geo_quorum_hardening.evacuation_chains import (
        build_rolling_evacuation_audit_chain,
    )
    from src.sports_signal_bot.geo_quorum_hardening.operator_coverage import (
        build_global_operator_coverage_synthesis,
    )
    from src.sports_signal_bot.geo_quorum_hardening.quorum_drills import (
        build_regional_quorum_drill,
    )

    # 1. Regional Quorum Drills
    drill = build_regional_quorum_drill(
        {
            "explicit_evidence": True,
            "stale_member_present": False,
            "unresolved_residue": False,
        }
    )
    save_artifact("regional_quorum_drills.json", [drill])

    # 2. Active-Passive Rehearsals
    rehearsal = build_active_passive_rehearsal(
        {
            "passive_stale": False,
            "unmeasured_readiness": False,
            "explicit_rollback_path": True,
        }
    )
    save_artifact("active_passive_rehearsals.json", [rehearsal])

    # 3. Global Operator Coverage Synthesis
    coverage = build_global_operator_coverage_synthesis(
        {
            "ownerless_critical_window": False,
            "escalation_unreachable": False,
            "stale_calendar_data": False,
        }
    )
    save_artifact("global_operator_coverage_synthesis.json", [coverage])

    # 4. Rolling Evacuation Audit Chains
    chain = build_rolling_evacuation_audit_chain(
        {
            "explicit_wave_scope": True,
            "broken_dependency": False,
            "no_safe_continuity_preserved": True,
        }
    )
    save_artifact("rolling_evacuation_audit_chains.json", [chain])

    return drill, rehearsal, coverage, chain


def _generate_summary_reports():
    import src.sports_signal_bot.geo_quorum_hardening.coverage_seams as cs
    import src.sports_signal_bot.geo_quorum_hardening.passive_checkpoints as pc
    import src.sports_signal_bot.geo_quorum_hardening.summaries as sm

    save_artifact(
        "passive_readiness_report.json",
        [pc.summarize_passive_state({})],
    )
    save_artifact(
        "coverage_seam_report.json",
        [cs.summarize_coverage_seams({})],
    )
    save_artifact(
        "geo_quorum_operational_matrix.json",
        sm.build_geo_quorum_operational_matrix({}),
    )


def _evaluate_and_save_manifest(
    strategy_name: str, drill: Any, rehearsal: Any, coverage: Any, chain: Any
) -> Any:
    strategy = get_strategy(strategy_name)
    manifest_inputs = {
        "quorum_sufficient": drill.quorum_status == "quorum_verified",
        "quorum_drill_refs": [drill.quorum_drill_id],
        "passive_stale": rehearsal.rehearsal_status == "rehearsal_blocked",
        "rehearsal_refs": [rehearsal.active_passive_rehearsal_id],
        "coverage_seam_gaps": (
            1 if coverage.synthesis_status != "coverage_synthesized" else 0
        ),
        "coverage_refs": [coverage.coverage_synthesis_id],
        "evacuation_refs": [chain.evacuation_chain_id],
    }
    manifest = strategy.evaluate(manifest_inputs)
    save_artifact("geo_quorum_hardening_manifest.json", manifest)

    health_report = {
        "overall_status": manifest.overall_status,
        "release_blockers": len(
            [
                w
                for w in manifest.warnings
                if "blocked" in manifest.overall_status
            ]
        ),
        "warnings": manifest.warnings,
    }
    save_artifact("geo_quorum_hardening_health_report.json", health_report)

    return manifest


def run_hardening_pass(strategy_name: str) -> Dict[str, Any]:
    from src.sports_signal_bot.geo_quorum_hardening.budgets import (
        summarize_geo_quorum_budgets,
    )

    drill, rehearsal, coverage, chain = _execute_core_hardening_processes()

    _generate_summary_reports()

    # 5. Budgets
    budget = summarize_geo_quorum_budgets({"quorum_erosion_breach": False})
    save_artifact("geo_quorum_budgets.json", budget)

    manifest = _evaluate_and_save_manifest(
        strategy_name, drill, rehearsal, coverage, chain
    )

    return manifest.model_dump()
