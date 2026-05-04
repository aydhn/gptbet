import pytest
from sports_signal_bot.governance_assurance.summaries import (
    summarize_council_marketplace_flow, summarize_debt_planner_flow
)

def test_reporting_summaries():
    flow1 = summarize_council_marketplace_flow("applied", "matched")
    assert flow1["overall_status"] == "flow_completed"

    flow2 = summarize_debt_planner_flow("caveated", "capped")
    assert flow2["overall_status"] == "flow_completed"
