import pytest
from sports_signal_bot.schema_governance.versions import SchemaVersionRecord

def test_semver_string():
    version = SchemaVersionRecord(
        schema_name="test",
        major_version=2,
        minor_version=1,
        patch_version=0,
        schema_version="v2.1.0"
    )
    assert version.version_string == "v2.1.0"
