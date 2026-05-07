import pytest
from src.sports_signal_bot.planetary_federation_hardening.scheduler_buses import (
    build_scheduler_bus, add_scheduler_bus_lane, build_scheduler_bus_packet, verify_scheduler_bus,
    BusFamily, BusStatus, SchedulerBusLaneRecord, SchedulerBusPacketRecord, SchedulerBusCadenceRecord
)

def test_verify_scheduler_bus_verified():
    bus = build_scheduler_bus("bus-01", BusFamily.PLANETARY_COVERAGE_SCHEDULER_BUS)
    add_scheduler_bus_lane(bus, SchedulerBusLaneRecord("lane-01", is_ownerless=False))
    bus.packet_refs.append(SchedulerBusPacketRecord("pkt-01", is_stale=False, has_ack=True))
    bus.cadence_refs.append(SchedulerBusCadenceRecord("cad-01", drift_ms=0))

    health = verify_scheduler_bus(bus)
    assert health.is_healthy
    assert health.status == BusStatus.BUS_VERIFIED

def test_verify_scheduler_bus_caveated():
    bus = build_scheduler_bus("bus-01", BusFamily.PLANETARY_COVERAGE_SCHEDULER_BUS)
    add_scheduler_bus_lane(bus, SchedulerBusLaneRecord("lane-01", is_ownerless=False))
    bus.packet_refs.append(SchedulerBusPacketRecord("pkt-01", is_stale=True, has_ack=True))
    bus.cadence_refs.append(SchedulerBusCadenceRecord("cad-01", drift_ms=500))

    health = verify_scheduler_bus(bus)
    assert not health.is_healthy
    assert health.status == BusStatus.BUS_CAVEATED

def test_verify_scheduler_bus_blocked():
    bus = build_scheduler_bus("bus-01", BusFamily.PLANETARY_COVERAGE_SCHEDULER_BUS)
    add_scheduler_bus_lane(bus, SchedulerBusLaneRecord("lane-01", is_ownerless=True))
    bus.packet_refs.append(SchedulerBusPacketRecord("pkt-01", is_stale=False, has_ack=False))

    health = verify_scheduler_bus(bus)
    assert not health.is_healthy
    assert health.status == BusStatus.BUS_BLOCKED
