from src.sports_signal_bot.supermesh_hardening.summaries import build_supermesh_fabric_matrix, validate_supermesh_fabric_row, summarize_supermesh_fabric_matrix, add_matrix_row

def test_matrix_validation():
    row_valid = {
        "owner_visible": True,
        "freshness_note_visible": True,
        "no_safe_visible": True,
        "sovereignty_note_visible": True,
        "residue_visible": True,
        "replayability_preserved": True
    }
    assert validate_supermesh_fabric_row(row_valid)

    row_invalid = {
        "owner_visible": True,
        "freshness_note_visible": True,
        "no_safe_visible": False,  # Note missing
        "sovereignty_note_visible": True,
        "residue_visible": True,
        "replayability_preserved": True
    }
    assert not validate_supermesh_fabric_row(row_invalid)

def test_matrix_summary():
    matrix = build_supermesh_fabric_matrix()
    add_matrix_row(matrix, {
        "owner_visible": True,
        "freshness_note_visible": True,
        "no_safe_visible": True,
        "sovereignty_note_visible": True,
        "residue_visible": True,
        "replayability_preserved": True
    })
    summary = summarize_supermesh_fabric_matrix(matrix)
    assert summary["total_rows"] == 1
    assert summary["valid_rows"] == 1
    assert summary["fully_compliant"] is True
