from sports_signal_bot.bankroll.contracts import (
    BankrollRunManifest,
    BankrollSummaryRecord,
    BankrollConfig,
    OverlayStrategyName,
)
import datetime
import os
import tempfile
from sports_signal_bot.bankroll.manifests import export_bankroll_manifest


def test_manifest_export():
    summary = BankrollSummaryRecord(
        initial_bankroll=1000,
        ending_bankroll=1100,
        net_pnl_units=100,
        return_pct=0.1,
        avg_stake_units=10,
        executed_count=10,
        win_rate=0.6,
        max_drawdown_pct=0.05,
        longest_loss_streak=2,
        longest_win_streak=3,
        average_pnl_per_decision=10,
    )
    manifest = BankrollRunManifest(
        run_id="test_run",
        timestamp=datetime.datetime.utcnow(),
        sport="s",
        market="m",
        overlay_strategy="flat_stake",
        config=BankrollConfig(),
        summary=summary,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        path = export_bankroll_manifest(manifest, tmpdir)
        assert os.path.exists(path)
