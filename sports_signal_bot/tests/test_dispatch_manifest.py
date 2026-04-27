import pytest
from pathlib import Path
from sports_signal_bot.telegram_dispatch.contracts import TelegramDispatchManifest
from sports_signal_bot.telegram_dispatch.manifests import ManifestWriter

def test_manifest_write(tmp_path):
    manifest = TelegramDispatchManifest(
        run_id="run-123",
        total_messages_rendered=5,
        total_messages_sent=4,
        suppressed_count=1
    )
    writer = ManifestWriter(tmp_path)
    file_path = writer.write_manifest(manifest)

    assert file_path.exists()
    import json
    with open(file_path) as f:
        data = json.load(f)
        assert data["run_id"] == "run-123"
        assert data["total_messages_rendered"] == 5
