import os
from sports_signal_bot.staged_channels.manifests import write_manifest, read_manifest

def test_manifest_rw(tmp_path):
    path = os.path.join(tmp_path, "manifest.json")
    data = [{"candidate": "c1", "status": "active"}]
    write_manifest(path, data)
    loaded = read_manifest(path)
    assert len(loaded) == 1
    assert loaded[0]["candidate"] == "c1"
