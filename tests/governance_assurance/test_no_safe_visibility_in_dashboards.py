import pytest
from sports_signal_bot.governance_assurance.contracts import DashboardFamily
from sports_signal_bot.governance_assurance.views import create_dashboard_view
from sports_signal_bot.governance_assurance.dashboards import build_governance_assurance_dashboard

def test_no_safe_visibility_enforcement():
    # If a view is missing 'no_safe_panel', it should have a warning
    view_without_nosafe = create_dashboard_view("v1", DashboardFamily.EXECUTIVE_SUMMARY, "execs", ["some_other_panel"])
    assert "missing_no_safe_visibility" in view_without_nosafe.warnings

    view_with_nosafe = create_dashboard_view("v2", DashboardFamily.EXECUTIVE_SUMMARY, "execs", ["no_safe_panel"])
    assert "missing_no_safe_visibility" not in view_with_nosafe.warnings
