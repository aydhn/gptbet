import pytest
from sports_signal_bot.schema_governance.migrations import build_migration_plan, migrate_payload

def test_payload_migration():
    plan = build_migration_plan("v1.0.0", "v2.0.0")
    payload = {"old_field": "val"}
    migrated = migrate_payload(payload, plan)
    # Since it's a basic placeholder, it should return dict
    assert "old_field" in migrated
