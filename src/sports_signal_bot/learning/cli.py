import typer
from rich.console import Console
from .contracts import (
    FeedbackSignalAggregateRecord,
    PatternCandidateRecord,
    SuggestionBundleRecord,
    RuleSuggestionRecordV2,
    AssimilationDecisionRecord,
    SuggestionSimulationRecord
)
# We would typically import logic handlers and strategies here
from .signals import FeedbackAggregator
from .patterns import PatternMiner
from .strategies.balanced_assimilation import BalancedAssimilationStrategy
from .assimilation import AssimilationEngine
from .simulation import SimulationManager

console = Console()
learning_app = typer.Typer(help="Phase 42 Learning and Feedback Assimilation Ops")

# Mock data functions for demonstration
def _mock_aggregates() -> list[FeedbackSignalAggregateRecord]:
    # Placeholder for a DB fetch
    import uuid
    return [
        FeedbackSignalAggregateRecord(
            aggregate_id=str(uuid.uuid4()),
            target_component_family="provider_trust",
            signal_type="provider_dispute_overturn",
            aggregated_cases=["case_1", "case_2", "case_3", "case_4"],
            total_signals=4,
            common_payload_elements={"action": "reduce_trust", "provider_id": "P_001"},
            time_span_days=14,
            contradictory_signals_count=0
        ),
         FeedbackSignalAggregateRecord(
            aggregate_id=str(uuid.uuid4()),
            target_component_family="threshold",
            signal_type="false_no_bet_correction",
            aggregated_cases=["case_10", "case_11"],
            total_signals=2,
            common_payload_elements={"action": "relax_threshold", "market": "ou_2_5"},
            time_span_days=5,
            contradictory_signals_count=0
        )
    ]

def _process_learning_pipeline():
    aggregates = _mock_aggregates()
    candidates = []
    for agg in aggregates:
        c = PatternMiner.build_pattern_candidate(agg)
        if c:
             candidates.append(c)

    strategy = BalancedAssimilationStrategy()
    bundle = strategy.process_candidates(candidates)

    decisions = []
    for sug in bundle.suggestions:
        decisions.append(AssimilationEngine.build_assimilation_decision(sug))

    return aggregates, candidates, bundle, decisions


@learning_app.command("run-learning-pass")
def run_learning_pass():
    """Run the feedback assimilation and suggestion generation pipeline."""
    console.print("[bold blue]Starting Phase 42 Learning Pass...[/bold blue]")
    aggregates, candidates, bundle, decisions = _process_learning_pipeline()

    console.print(f"Aggregated Feedback Signals: {len(aggregates)}")
    console.print(f"Pattern Candidates Extracted: {len(candidates)}")
    console.print(f"Suggestions Generated: {len(bundle.suggestions)}")

    advisory = sum(1 for s in bundle.suggestions if s.recommendation_mode == "advisory_only")
    patches = sum(1 for s in bundle.suggestions if s.recommendation_mode == "candidate_patch")
    reviews = sum(1 for s in bundle.suggestions if s.recommendation_mode == "manual_review_required")

    console.print("\n[bold]Suggestion Breakdown:[/bold]")
    console.print(f"  Advisory Only: {advisory}")
    console.print(f"  Candidate Patches: {patches}")
    console.print(f"  Manual Review Required: {reviews}")

    console.print("\n[bold green]Learning pass complete. Artifacts ready for review.[/bold green]")

@learning_app.command("preview-pattern-candidates")
def preview_pattern_candidates():
    """Preview pattern candidates generated from feedback."""
    aggregates, candidates, bundle, decisions = _process_learning_pipeline()
    for c in candidates:
        console.print(f"ID: {c.pattern_id}")
        console.print(f"Family: {c.component_family}")
        console.print(f"Action: {c.candidate_action}")
        console.print(f"Support: {c.support.strength.value} ({c.support.support_count} cases)")
        console.print("---")

@learning_app.command("preview-tuning-suggestions")
def preview_tuning_suggestions():
    """Preview structured tuning suggestions."""
    aggregates, candidates, bundle, decisions = _process_learning_pipeline()
    for s in bundle.suggestions:
        console.print(f"ID: {s.suggestion_id}")
        console.print(f"Family: {s.suggestion_family.value}")
        console.print(f"Risk: {s.estimated_risk.risk_level.value}")
        console.print(f"Confidence: {s.confidence_score.confidence_band.value}")
        console.print(f"Mode: {s.recommendation_mode.value}")
        if s.structured_rule:
            from .extraction import RuleExtractor
            console.print(f"Rule: {RuleExtractor.render_rule_preview(s.structured_rule)}")
        console.print("---")

@learning_app.command("preview-assimilation-decisions")
def preview_assimilation_decisions():
    """Preview assimilation decisions and routing."""
    aggregates, candidates, bundle, decisions = _process_learning_pipeline()
    for d in decisions:
        console.print(f"Suggestion: {d.suggestion_id}")
        console.print(f"Status: {d.decision_status.value}")
        console.print(f"Route: {d.assigned_review_route}")
        console.print(f"Sim Required: {d.simulation_required}")
        console.print(f"Rationale: {d.rationale}")
        console.print("---")

@learning_app.command("list-learning-strategies")
def list_learning_strategies():
    """List available learning strategies."""
    console.print("Available Strategies:")
    console.print("1. ConservativeSuggestionStrategy")
    console.print("2. BalancedAssimilationStrategy (Default)")
    console.print("3. AdvisoryFirstStrategy")
    console.print("4. AliasAndProviderFocusedStrategy")
    console.print("5. PolicyBoundaryFocusedStrategy")
