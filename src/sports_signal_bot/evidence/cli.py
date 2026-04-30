import typer
import json
from pathlib import Path
from sports_signal_bot.evidence.builders.decision import DecisionEvidenceBuilder
from sports_signal_bot.evidence.builders.why_not import WhyNotEvidenceBuilder
from sports_signal_bot.evidence.claims import build_claim
from sports_signal_bot.evidence.citations import build_citation_trail
from sports_signal_bot.evidence.explanations import explain_why_decision, explain_why_not
from sports_signal_bot.evidence.registry import StrategyRegistry
from sports_signal_bot.evidence.counterfactuals import generate_threshold_counterfactual

app = typer.Typer(help="Evidence and Explainability Commands")

@app.command("build-evidence-bundles")
def build_bundles_cmd(sport: str = "football", market: str = "1x2"):
    typer.echo(f"Building evidence bundles for {sport} - {market}")
    builder = DecisionEvidenceBuilder("event_sample_123", audience_profile="auditor_full")

    cit1 = build_citation_trail("cit_1", "provider_observation", "pinnacle", "ref_x", "art_y", "man_z", notes="High liquidity market")
    claim1 = build_claim("claim_1", "prediction_claim", "Model strongly predicts Home Win", "high", 0.92)
    claim1.citation_refs.append(cit1.citation_id)

    builder.add_citation(cit1)
    builder.add_claim(claim1)

    bundle = builder.build()

    Path("results").mkdir(exist_ok=True)
    with open("results/evidence_bundles.json", "w") as f:
        f.write(bundle.model_dump_json(indent=2))

    typer.echo(f"Bundle {bundle.bundle_id} created with status {bundle.evidence_status}")

@app.command("explain-decision")
def explain_decision_cmd(event_id: str):
    builder = DecisionEvidenceBuilder(event_id, audience_profile="operator_concise")
    claim1 = build_claim("claim_1", "prediction_claim", "Signal score crossed threshold", "high", 0.88)
    builder.add_claim(claim1)
    bundle = builder.build()

    explanation = explain_why_decision(bundle, "Approval rationale")
    typer.echo(f"Decision Explanation for {event_id}:")
    typer.echo(explanation)

@app.command("explain-why-not")
def explain_why_not_cmd(event_id: str):
    builder = WhyNotEvidenceBuilder(event_id, audience_profile="reviewer_standard")
    claim1 = build_claim("claim_1", "policy_claim", "Blocked by maximum exposure limits", "high", 1.0)
    builder.add_claim(claim1)
    bundle = builder.build()

    explanation = explain_why_not(bundle, [claim1.claim_text])
    typer.echo(f"Why Not Explanation for {event_id}:")
    typer.echo(explanation)

@app.command("preview-citation-trails")
def preview_citation_trails_cmd(event_id: str):
    cit1 = build_citation_trail("cit_1", "feature_ref", "elo_engine", "elo_event_1", "art_elo", "man_elo", notes="Elo ratings pre-match snapshot")
    typer.echo(f"Citation Trail for {event_id}:")
    typer.echo(json.dumps(cit1.model_dump(), indent=2))

@app.command("preview-counterfactual-hints")
def preview_counterfactuals_cmd(event_id: str):
    hint = generate_threshold_counterfactual(current_score=0.75, required_threshold=0.80)
    typer.echo(f"Counterfactual Hints for {event_id}:")
    typer.echo(json.dumps(hint.model_dump(), indent=2))

@app.command("list-explainability-strategies")
def list_strategies_cmd():
    registry = StrategyRegistry()
    typer.echo("Available Explainability Strategies:")
    for strategy in registry.list_strategies():
        typer.echo(f"- {strategy}")

if __name__ == "__main__":
    app()
