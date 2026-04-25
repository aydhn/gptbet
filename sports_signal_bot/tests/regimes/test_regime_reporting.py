import os

import pytest

from sports_signal_bot.regimes.contracts import RegimeManifest
from sports_signal_bot.regimes.reporting import (export_regime_manifest,
                                                 generate_regime_summary)


def test_regime_reporting(tmp_path):
    manifest = RegimeManifest(run_id="test", active_families=["form"])
    path = tmp_path / "manifest.json"
    export_regime_manifest(manifest, str(path))
    assert os.path.exists(path)

    summary = generate_regime_summary(manifest)
    assert "Family: form" in summary
