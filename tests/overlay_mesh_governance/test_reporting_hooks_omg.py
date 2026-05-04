import pytest
import os
from sports_signal_bot.overlay_mesh_governance.reporting import (
    generate_overlay_mesh_governance_summary,
    export_overlay_mesh_governance_summary
)

def test_generate_and_export_summary(tmp_path):
    summary = generate_overlay_mesh_governance_summary()
    assert summary["overall_health"] == "healthy"

    filepath = os.path.join(tmp_path, "summary.json")
    export_overlay_mesh_governance_summary(filepath, summary)
    assert os.path.exists(filepath)
