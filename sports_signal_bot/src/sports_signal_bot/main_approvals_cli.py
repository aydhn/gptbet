import typer
from rich.console import Console
from datetime import datetime, timezone
import json
from pathlib import Path

from sports_signal_bot.approvals.contracts import (
    ApprovalRequestRecord, OperatorIdentityRecord, RequestType, ApprovalScope, OverrideType, OverrideRecord, OverrideScopeRecord
)
from sports_signal_bot.approvals.registry import ApprovalRegistry
from sports_signal_bot.approvals.runner import ApprovalRunner
from sports_signal_bot.approvals.freeze_release import FreezeReleaseManager
from sports_signal_bot.approvals.acknowledgements import acknowledge_alert
from sports_signal_bot.core.paths import get_data_dir

app = typer.Typer(help="Operator Approval Workflow CLI")
console = Console()

def get_registry() -> ApprovalRegistry:
    return ApprovalRegistry(str(get_data_dir() / "approvals"))

def get_runner() -> ApprovalRunner:
    return ApprovalRunner(get_registry())

def get_operator(operator_id: str) -> OperatorIdentityRecord:
    # Minimal mock logic. In real system, this would load from a configured registry.
    roles = {"admin1": "admin", "senior1": "senior_operator", "ops1": "operator", "rev1": "reviewer"}
    if operator_id not in roles:
        raise ValueError(f"Unknown operator: {operator_id}")
    return OperatorIdentityRecord(
        operator_id=operator_id,
        display_name=operator_id.capitalize(),
        role=roles[operator_id],
        active=True
    )

@app.command()
def list_review_items():
    """List open review items."""
    reg = get_registry()
    items = []
    for path in reg.storage_dir.glob("request_*.json"):
        with open(path, "r") as f:
            req = ApprovalRequestRecord.model_validate_json(f.read())
            if req.status == "pending_review":
                items.append(req)
    console.print(f"Found {len(items)} pending approval requests.")
    for req in items:
        console.print(f"- {req.request_id}: {req.request_type.value} for {req.target_entity_type} {req.target_entity_id}")

@app.command()
def show_approval_request(request_id: str = typer.Option(...)):
    """Show details of an approval request."""
    reg = get_registry()
    path = reg.storage_dir / f"request_{request_id}.json"
    if not path.exists():
        console.print(f"[red]Request {request_id} not found[/red]")
        return
    with open(path, "r") as f:
        req = ApprovalRequestRecord.model_validate_json(f.read())
    console.print(req.model_dump_json(indent=2))

@app.command()
def approve_request(request_id: str = typer.Option(...), operator_id: str = typer.Option(...), note: str = typer.Option("Approved")):
    """Approve a request."""
    reg = get_registry()
    runner = get_runner()
    path = reg.storage_dir / f"request_{request_id}.json"
    if not path.exists():
        console.print(f"[red]Request {request_id} not found[/red]")
        return
    with open(path, "r") as f:
        req = ApprovalRequestRecord.model_validate_json(f.read())

    if req.status != "pending_review":
         console.print(f"[red]Request {request_id} is already {req.status.value}[/red]")
         return

    try:
        op = get_operator(operator_id)
        decision = runner.process_decision(req, op, "approve", note)
        console.print(f"[green]Request {request_id} approved. Decision ID: {decision.decision_id}[/green]")
    except Exception as e:
        console.print(f"[red]Failed to approve: {e}[/red]")

@app.command()
def reject_request(request_id: str = typer.Option(...), operator_id: str = typer.Option(...), note: str = typer.Option("Rejected")):
    """Reject a request."""
    reg = get_registry()
    runner = get_runner()
    path = reg.storage_dir / f"request_{request_id}.json"
    if not path.exists():
        console.print(f"[red]Request {request_id} not found[/red]")
        return
    with open(path, "r") as f:
        req = ApprovalRequestRecord.model_validate_json(f.read())

    if req.status != "pending_review":
         console.print(f"[red]Request {request_id} is already {req.status.value}[/red]")
         return

    try:
        op = get_operator(operator_id)
        decision = runner.process_decision(req, op, "reject", note)
        console.print(f"[green]Request {request_id} rejected. Decision ID: {decision.decision_id}[/green]")
    except Exception as e:
        console.print(f"[red]Failed to reject: {e}[/red]")

@app.command()
def defer_request(request_id: str = typer.Option(...), operator_id: str = typer.Option(...), note: str = typer.Option("Deferred")):
    """Defer a request."""
    reg = get_registry()
    runner = get_runner()
    path = reg.storage_dir / f"request_{request_id}.json"
    if not path.exists():
        console.print(f"[red]Request {request_id} not found[/red]")
        return
    with open(path, "r") as f:
        req = ApprovalRequestRecord.model_validate_json(f.read())

    if req.status != "pending_review":
         console.print(f"[red]Request {request_id} is already {req.status.value}[/red]")
         return

    try:
        op = get_operator(operator_id)
        decision = runner.process_decision(req, op, "defer", note)
        console.print(f"[green]Request {request_id} deferred. Decision ID: {decision.decision_id}[/green]")
    except Exception as e:
        console.print(f"[red]Failed to defer: {e}[/red]")

@app.command()
def create_override(type: str = typer.Option(...), operator_id: str = typer.Option(...), reason: str = typer.Option("Manual override")):
    """Create an override."""
    try:
        ov_type = OverrideType(type)
        op = get_operator(operator_id)
        # Assuming admin/senior check for override creation
        if op.role not in ["admin", "senior_operator"]:
            raise PermissionError("Insufficient permissions to create override")

        import uuid
        ov = OverrideRecord(
            override_id=f"ov_{uuid.uuid4().hex[:8]}",
            override_type=ov_type,
            operator_id=operator_id,
            scope=OverrideScopeRecord(scope_type=ApprovalScope.temporary_override_window),
            reason=reason
        )
        get_registry().save_override(ov)
        console.print(f"[green]Override created: {ov.override_id}[/green]")
    except Exception as e:
        console.print(f"[red]Failed to create override: {e}[/red]")

@app.command()
def revoke_override(override_id: str = typer.Option(...), operator_id: str = typer.Option(...)):
    """Revoke an override."""
    reg = get_registry()
    path = reg.storage_dir / f"override_{override_id}.json"
    if not path.exists():
        console.print(f"[red]Override {override_id} not found[/red]")
        return

    try:
        op = get_operator(operator_id)
        if op.role != "admin":
             raise PermissionError("Only admin can revoke overrides")

        with open(path, "r") as f:
            ov = OverrideRecord.model_validate_json(f.read())

        ov.status = "revoked"
        reg.save_override(ov)
        console.print(f"[green]Override {override_id} revoked.[/green]")
    except Exception as e:
        console.print(f"[red]Failed to revoke: {e}[/red]")

@app.command()
def request_freeze_release(operator_id: str = typer.Option(...), reason: str = typer.Option("System looks good")):
    """Request a freeze release."""
    try:
        get_operator(operator_id) # validates operator
        req = FreezeReleaseManager.create_request(operator_id, reason)
        # Create an approval request for the freeze release
        from sports_signal_bot.approvals.workflows.freeze_release_review import build_freeze_release_review_request
        approval_req = build_freeze_release_review_request(
            freeze_id=req.request_id,
            origin_component="cli",
            rationale=reason
        )
        get_registry().save_request(approval_req)
        console.print(f"[green]Freeze release requested. Request ID: {approval_req.request_id}[/green]")
    except Exception as e:
         console.print(f"[red]Failed to request freeze release: {e}[/red]")

@app.command()
def approve_freeze_release(request_id: str = typer.Option(...), operator_id: str = typer.Option(...), note: str = typer.Option("Approved release")):
    """Approve a freeze release."""
    reg = get_registry()
    runner = get_runner()
    path = reg.storage_dir / f"request_{request_id}.json"
    if not path.exists():
        console.print(f"[red]Request {request_id} not found[/red]")
        return
    with open(path, "r") as f:
        req = ApprovalRequestRecord.model_validate_json(f.read())

    if req.request_type != "approve_freeze_release":
        console.print(f"[red]Request {request_id} is not a freeze release request[/red]")
        return

    try:
        # Dummy prerequisites validation
        if not FreezeReleaseManager.validate_prerequisites(0, True):
            raise ValueError("Prerequisites for freeze release not met.")

        op = get_operator(operator_id)
        decision = runner.process_decision(req, op, "approve", note)
        console.print(f"[green]Freeze release {request_id} approved. Decision ID: {decision.decision_id}[/green]")
    except Exception as e:
        console.print(f"[red]Failed to approve freeze release: {e}[/red]")

@app.command()
def acknowledge_alert(alert_id: str = typer.Option(...), operator_id: str = typer.Option(...), note: str = typer.Option("Acknowledged")):
    """Acknowledge an alert."""
    try:
        get_operator(operator_id)
        ack = acknowledge_alert(alert_id, operator_id, note)
        console.print(f"[green]Alert {alert_id} acknowledged. Ack ID: {ack.ack_id}[/green]")
    except Exception as e:
         console.print(f"[red]Failed to acknowledge alert: {e}[/red]")

@app.command()
def preview_active_overrides():
    """Preview active overrides."""
    reg = get_registry()
    active = []
    for path in reg.storage_dir.glob("override_*.json"):
        with open(path, "r") as f:
            ov = OverrideRecord.model_validate_json(f.read())
            if ov.status == "active":
                active.append(ov)
    console.print(f"Found {len(active)} active overrides:")
    for ov in active:
        console.print(f"- {ov.override_id}: {ov.override_type.value} (by {ov.operator_id})")

@app.command()
def preview_approval_audit():
    """Preview approval audit ledger."""
    reg = get_registry()
    audit_path = reg.storage_dir / "audit_ledger.csv"
    if not audit_path.exists():
        console.print("No audit ledger found.")
        return
    import csv
    with open(audit_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    console.print(f"Found {len(rows)} audit ledger entries.")
    for i, row in enumerate(rows[-5:]):
        console.print(f"{row['timestamp']}: {row['action']} on {row['entity_type']} {row['entity_id']} by {row['operator_id']}")

if __name__ == "__main__":
    app()
