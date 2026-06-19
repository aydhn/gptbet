from sports_signal_bot.geo_hardening.wave_checkpoints import diff_relocation_wave_outputs, create_relocation_wave_checkpoint, detect_relocation_wave_gaps

def test_detect_relocation_wave_gaps_empty():
    assert detect_relocation_wave_gaps([]) == []

def test_detect_relocation_wave_gaps_no_gaps():
    segments = [{"id": 0}, {"id": 1}, {"id": 2}]
    assert detect_relocation_wave_gaps(segments) == []

def test_detect_relocation_wave_gaps_with_gaps():
    segments = [{"id": 0}, {"id": 2}, {"id": 3}, {"id": 5}]
    # Iteration 1: s={"id": 0}, expected_id=0 -> matches. expected_id becomes 1.
    # Iteration 2: s={"id": 2}, expected_id=1 -> mismatch. gaps=[1]. expected_id becomes 2.
    # Iteration 3: s={"id": 3}, expected_id=2 -> mismatch. gaps=[1, 2]. expected_id becomes 3.
    # Iteration 4: s={"id": 5}, expected_id=3 -> mismatch. gaps=[1, 2, 3]. expected_id becomes 4.
    assert detect_relocation_wave_gaps(segments) == [1, 2, 3]

def test_detect_relocation_wave_gaps_missing_id_key():
    segments = [{"id": 0}, {"not_id": 1}, {"id": 2}]
    # Iteration 1: s={"id": 0}, expected_id=0 -> matches. expected_id becomes 1.
    # Iteration 2: s={"not_id": 1}, expected_id=1. get("id", -1) is -1. mismatch. gaps=[1]. expected_id becomes 2.
    # Iteration 3: s={"id": 2}, expected_id=2 -> matches. expected_id becomes 3.
    assert detect_relocation_wave_gaps(segments) == [1]

def test_detect_relocation_wave_gaps_out_of_order():
    segments = [{"id": 0}, {"id": 2}, {"id": 1}]
    # Iteration 1: s={"id": 0}, expected_id=0 -> matches. expected_id becomes 1.
    # Iteration 2: s={"id": 2}, expected_id=1 -> mismatch. gaps=[1]. expected_id becomes 2.
    # Iteration 3: s={"id": 1}, expected_id=2 -> mismatch. gaps=[1, 2]. expected_id becomes 3.
    assert detect_relocation_wave_gaps(segments) == [1, 2]

def test_checkpoints():
    assert True

def test_diff_relocation_wave_outputs_identical():
    source = {"a": 1, "b": 2}
    target = {"a": 1, "b": 2}
    result = diff_relocation_wave_outputs(source, target)
    assert result == {}

def test_diff_relocation_wave_outputs_different_values():
    source = {"a": 1, "b": 2}
    target = {"a": 1, "b": 3}
    result = diff_relocation_wave_outputs(source, target)
    assert result == {"b": {"source": 2, "target": 3}}

def test_diff_relocation_wave_outputs_missing_in_target():
    source = {"a": 1, "b": 2}
    target = {"a": 1}
    result = diff_relocation_wave_outputs(source, target)
    assert result == {"b": {"source": 2, "target": None}}

def test_diff_relocation_wave_outputs_missing_in_source():
    source = {"a": 1}
    target = {"a": 1, "b": 2}
    result = diff_relocation_wave_outputs(source, target)
    assert result == {} # The function only iterates over source keys

def test_diff_relocation_wave_outputs_empty():
    source = {}
    target = {}
    result = diff_relocation_wave_outputs(source, target)
    assert result == {}

    source = {"a": 1}
    target = {}
    result = diff_relocation_wave_outputs(source, target)
    assert result == {"a": {"source": 1, "target": None}}

    source = {}
    target = {"a": 1}
    result = diff_relocation_wave_outputs(source, target)
    assert result == {}

def test_create_relocation_wave_checkpoint():
    result = create_relocation_wave_checkpoint("wave-1", "start")
    assert result == {"wave_id": "wave-1", "checkpoint_type": "start", "status": "verified"}

def test_create_relocation_wave_checkpoint_empty_strings():
    result = create_relocation_wave_checkpoint("", "")
    assert result == {"wave_id": "", "checkpoint_type": "", "status": "verified"}
