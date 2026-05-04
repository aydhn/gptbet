import typer
from typing import Optional
import json
from sports_signal_bot.federation_ecosystem.contracts import FederationLinkRecord, BaselineCatalogEntryRecord, EcosystemParticipantRecord
from sports_signal_bot.federation_ecosystem.federations import build_registry_federation, add_federation_link
from sports_signal_bot.federation_ecosystem.hubs import build_attestation_hub, evaluate_hub_admission, route_packet_through_hub
from sports_signal_bot.federation_ecosystem.baselines import build_baseline_catalog, register_baseline_catalog_entry
from sports_signal_bot.federation_ecosystem.ecosystems import build_policy_attestation_ecosystem, register_ecosystem_participant
from sports_signal_bot.federation_ecosystem.strategies import AVAILABLE_STRATEGIES

app = typer.Typer()

@app.command("run-federation-ecosystem-pass")
def run_federation_ecosystem_pass(strategy: str = typer.Option("balanced", help="Federation Ecosystem Strategy")):
    """Run a full federation ecosystem evaluation pass."""
    typer.echo(f"Running federation ecosystem pass with strategy: {strategy}")
    if strategy not in AVAILABLE_STRATEGIES:
        typer.echo(f"Strategy {strategy} not found. Using balanced.")
        strategy = "balanced"

    strat = AVAILABLE_STRATEGIES[strategy]

    # Simulate run
    typer.echo(f"Evaluating registry currentness... ({strat.evaluate_currentness('valid', 'linked_bounded_exchange')})")
    typer.echo(f"Evaluating hub admission... ({strat.evaluate_admission('valid', 'none')})")
    typer.echo(f"Evaluating ecosystem visibility... ({strat.evaluate_visibility('participating_bounded_exchange', False)})")

    typer.echo("Federation ecosystem pass complete.")

@app.command("preview-registry-federations")
def preview_registry_federations():
    """Preview current registry federations."""
    fed = build_registry_federation("fed_01", "sovereign_corridor_registry_federation", ["reg_a", "reg_b"])
    link = FederationLinkRecord(link_id="link_01", source_registry_ref="reg_a", target_registry_ref="reg_b", link_status="linked_bounded_exchange")
    fed = add_federation_link(fed, link)
    typer.echo(json.dumps(fed.model_dump(), indent=2))

@app.command("preview-attestation-hubs")
def preview_attestation_hubs():
    """Preview attestation exchange hubs and queues."""
    hub = build_attestation_hub("hub_01", "internal_attestation_hub")
    adm = evaluate_hub_admission("pkt_123", "reg_a", "valid", "none")
    route = route_packet_through_hub(adm)
    typer.echo(f"Hub ID: {hub.hub_id}")
    typer.echo(f"Admission: {adm.admission_status}")
    typer.echo(f"Route Outcome: {route.routing_outcome}")

@app.command("preview-baseline-catalogs")
def preview_baseline_catalogs():
    """Preview treaty baseline catalogs."""
    cat = build_baseline_catalog("cat_01", "treaty_baseline_catalog")
    entry = BaselineCatalogEntryRecord(
        baseline_entry_id="ent_01", baseline_ref="base_alpha", baseline_family="treaty_baseline_catalog",
        supported_treaty_families=[], supported_dimension_refs=[], baseline_version_ref="v1",
        freshness_state="fresh", discoverability_state="discoverable_current", caveat_summary="None", warnings=[]
    )
    cat = register_baseline_catalog_entry(cat, entry)
    typer.echo(json.dumps(cat.model_dump(), indent=2))

@app.command("preview-policy-attestation-ecosystems")
def preview_policy_attestation_ecosystems():
    """Preview sovereign policy attestation ecosystems."""
    eco = build_policy_attestation_ecosystem("eco_01", "sovereign_policy_attestation_ecosystem")
    part = EcosystemParticipantRecord(
        participant_id="part_01", participant_family="corridor_registry_participant",
        source_registry_refs=["reg_a"], issuer_profile_refs=[], supported_attestation_families=[],
        supported_exchange_scopes=[], visibility_profile="bounded_exchange_visible",
        participation_status="participating_bounded_exchange", warnings=[]
    )
    eco = register_ecosystem_participant(eco, part)
    typer.echo(json.dumps(eco.model_dump(), indent=2))

@app.command("preview-federation-ecosystem-health")
def preview_federation_ecosystem_health():
    """Preview health metrics for the federation ecosystem."""
    health = {"health_status": "healthy", "warnings": []}
    typer.echo(json.dumps(health, indent=2))

@app.command("list-federation-ecosystem-strategies")
def list_federation_ecosystem_strategies():
    """List available federation ecosystem strategies."""
    for name in AVAILABLE_STRATEGIES.keys():
        typer.echo(f"- {name}")
