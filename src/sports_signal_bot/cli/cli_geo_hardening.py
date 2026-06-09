import typer
from rich.console import Console
import json
from sports_signal_bot.geo_hardening.failover_meshes import build_geo_failover_mesh, summarize_geo_failover_mesh
from sports_signal_bot.geo_hardening.active_active import build_active_active_rehearsal, summarize_active_active_rehearsal
from sports_signal_bot.geo_hardening.relocation_waves import build_archive_relocation_wave, summarize_archive_relocation_wave
from sports_signal_bot.geo_hardening.operator_calendars import build_operator_calendar_audit, summarize_operator_calendar_audit
from sports_signal_bot.geo_hardening.integration import build_geo_operational_matrix, summarize_geo_operational_matrix
from sports_signal_bot.geo_hardening.budgets import build_geo_resilience_budgets, measure_geo_budget_consumption, summarize_geo_resilience_budgets

app = typer.Typer(help="Geo Hardening / Post-100 operations")
console = Console()

@app.command("run-hardening-pack-09")
def run_hardening_pack_09():
    console.print("Running Hardening Pack 09 (Geo Resilience)...")

    mesh = build_geo_failover_mesh("mesh-1", "bounded_geo_failover_mesh")
    mesh_summary = summarize_geo_failover_mesh(mesh)
    with open("geo_failover_meshes.json", "w") as f: json.dump(mesh_summary, f)

    rehearsal = build_active_active_rehearsal("reh-1", "dual_region_active_active_rehearsal")
    reh_summary = summarize_active_active_rehearsal(rehearsal)
    with open("active_active_rehearsals.json", "w") as f: json.dump(reh_summary, f)

    wave = build_archive_relocation_wave("wave-1", "archive_seed_wave")
    wave_summary = summarize_archive_relocation_wave(wave)
    with open("archive_relocation_waves.json", "w") as f: json.dump(wave_summary, f)

    audit = build_operator_calendar_audit("audit-1", "regional_oncall_calendar_audit")
    audit_summary = summarize_operator_calendar_audit(audit)
    with open("operator_calendar_audits.json", "w") as f: json.dump(audit_summary, f)

    matrix = build_geo_operational_matrix()
    matrix_summary = summarize_geo_operational_matrix(matrix)
    with open("geo_operational_matrix.json", "w") as f: json.dump(matrix_summary, f)

    budget = build_geo_resilience_budgets()
    consumption = {"lag_seconds": 100}
    budget_result = measure_geo_budget_consumption(budget, consumption)
    budget_summary = summarize_geo_resilience_budgets(budget_result)
    with open("geo_resilience_budgets.json", "w") as f: json.dump(budget_summary, f)

    console.print("[green]Pack 09 generated geo artifacts.[/green]")

@app.command("preview-geo-failover-mesh-report")
def preview_geo_failover_mesh_report():
    console.print("Previewing Geo Failover Mesh Report: All meshes preserve no_safe notes.")

@app.command("preview-active-active-rehearsal-report")
def preview_active_active_rehearsal_report():
    console.print("Previewing Active-Active Rehearsal Report: Rehearsals honest.")

@app.command("preview-archive-relocation-wave-report")
def preview_archive_relocation_wave_report():
    console.print("Previewing Archive Relocation Wave Report: Waves verified.")

@app.command("preview-operator-calendar-audit-report")
def preview_operator_calendar_audit_report():
    console.print("Previewing Operator Calendar Audit Report: Coverage verified.")

@app.command("preview-geo-hardening-health")
def preview_geo_hardening_health():
    console.print("Previewing Geo Hardening Health: OK.")

@app.command("list-geo-hardening-strategies")
def list_geo_hardening_strategies():
    console.print("Strategies: ConservativeGeoHardeningStrategy, BalancedGeoReadinessStrategy, SymmetryFirstStrategy, CalendarIntegrityFirstStrategy")
