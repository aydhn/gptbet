from typing import Dict, Any

def summarize_council_marketplace_flow(council_res: str, market_res: str) -> Dict[str, Any]:
    return {
        "council_outcome": council_res,
        "market_outcome": market_res,
        "overall_status": "flow_completed"
    }

def summarize_debt_planner_flow(planner_res: str, compiler_res: str) -> Dict[str, Any]:
    return {
        "planner_outcome": planner_res,
        "compiler_outcome": compiler_res,
        "overall_status": "flow_completed"
    }
