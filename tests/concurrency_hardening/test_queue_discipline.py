import pytest
from sports_signal_bot.concurrency_hardening.queues import build_queue_discipline, sample_queue_pressure, detect_queue_overflow_or_starvation

def test_build_queue_discipline():
    discipline = build_queue_discipline("q1")
    assert discipline.target_queue == "q1"
    assert discipline.status == "monitored"

def test_detect_queue_overflow_or_starvation():
    discipline = build_queue_discipline("q1")
    sample_overflow = sample_queue_pressure(100)
    overflow = detect_queue_overflow_or_starvation(discipline, sample_overflow, 50)
    assert overflow is not None
    assert overflow.dropped_items == 50
    assert discipline.status == "overflowing"

    discipline2 = build_queue_discipline("q2")
    sample_starved = sample_queue_pressure(0)
    detect_queue_overflow_or_starvation(discipline2, sample_starved, 50)
    assert discipline2.status == "monitored" # starvation doesn't change status, just adds warning
    assert len(discipline2.warnings) == 1
