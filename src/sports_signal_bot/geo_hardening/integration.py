from typing import Any, Dict


def build_geo_operational_matrix() -> Dict[str, Any]:
    return {
        "surfaces": [
            "geo_failover_meshes",
            "regional_failover_drills",
            "active_active_rehearsals",
            "archive_relocation_waves",
        ],
        "rows": [],
    }


def validate_geo_operational_row(
    matrix: Dict[str, Any], row: Dict[str, Any]
) -> Dict[str, Any]:
    matrix["rows"].append(row)
    return matrix


def summarize_geo_operational_matrix(matrix: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "total_surfaces": len(matrix.get("surfaces", [])),
        "total_rows": len(matrix.get("rows", [])),
        "status": "ready" if len(matrix.get("rows", [])) > 0 else "empty",
    }
