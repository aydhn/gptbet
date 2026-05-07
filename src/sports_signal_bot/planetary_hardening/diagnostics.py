def generate_health_report(matrix_summary: dict, budget_summary: dict) -> dict:
    total_issues = budget_summary.get("breaches_count", 0)
    status = "healthy" if total_issues == 0 else "needs_attention"
    return {
        "overall_status": status,
        "total_breaches": total_issues,
        "matrix": matrix_summary
    }
