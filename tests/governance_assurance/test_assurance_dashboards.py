import pytest
from sports_signal_bot.governance_assurance.contracts import DashboardFamily, PanelFamily
from sports_signal_bot.governance_assurance.dashboards import (
    build_governance_assurance_dashboard, summarize_dashboard_health
)
from sports_signal_bot.governance_assurance.views import create_dashboard_view
from sports_signal_bot.governance_assurance.panels import create_dashboard_panel

def test_build_governance_assurance_dashboard():
    dash = build_governance_assurance_dashboard("dash1", DashboardFamily.EXECUTIVE_SUMMARY)
    assert dash.dashboard_id == "dash1"

def test_create_dashboard_components():
    panel = create_dashboard_panel("pan1", PanelFamily.NO_SAFE_VISIBILITY, ["met1"])
    assert panel.panel_family == PanelFamily.NO_SAFE_VISIBILITY

    view = create_dashboard_view("v1", DashboardFamily.OPERATOR_ASSURANCE, "operators", ["pan1"])
    assert "missing_no_safe_visibility" in view.warnings # pan1 is NO_SAFE_VISIBILITY, but ref checking is mock
