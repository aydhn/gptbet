from typing import Optional

def generate_label_name(market_type: str, line: Optional[float] = None) -> str:
    """
    Deterministically generate a label name.
    e.g., football_1x2
    e.g., football_ou_2_5
    """
    base = market_type.lower()
    # Normalize market types for naming if needed, e.g., 'football_over_under' -> 'football_ou'
    base = base.replace("_over_under", "_ou")
    base = base.replace("_total_points", "_total")

    if line is not None:
        # replace decimal point with underscore for clean naming
        line_str = str(line).replace('.', '_')
        return f"{base}_{line_str}"
    return base
