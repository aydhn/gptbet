import pytest
import datetime
from sports_signal_bot.docs_ops.registry import DocRegistry
from sports_signal_bot.docs_ops.freshness import FreshnessReporter

def test_stale_doc(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    test_doc = docs_dir / "old_doc.md"

    old_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=40)).isoformat()
    test_doc.write_text(f"""---
title: "Old Doc"
doc_family: "overview"
owner_role: "ops"
freshness_window_days: 30
last_updated_at: "{old_date}"
---
# Old Doc
""")

    registry = DocRegistry(str(docs_dir))
    registry.scan()
    reporter = FreshnessReporter(registry)
    results = reporter.check_all()
    assert len(results) == 1
    assert results[0].is_stale
