import pytest
from sports_signal_bot.docs_ops.registry import DocRegistry
from sports_signal_bot.docs_ops.contracts import DocFamily

def test_registry_scan(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    test_doc = docs_dir / "test_runbook.md"
    test_doc.write_text("""---
title: "Test Runbook"
doc_family: "runbook"
status: "active"
---
# Test Runbook
""")

    registry = DocRegistry(str(docs_dir))
    registry.scan()
    docs = registry.list_documents()
    assert len(docs) == 1
    assert docs[0].title == "Test Runbook"
    assert docs[0].doc_family == DocFamily.RUNBOOK
