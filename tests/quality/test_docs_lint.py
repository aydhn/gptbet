import pytest
from sports_signal_bot.docs_ops.registry import DocRegistry
from sports_signal_bot.docs_ops.lint import DocLintRunner

def test_missing_required_section(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    test_doc = docs_dir / "test_runbook.md"
    test_doc.write_text("""---
title: "Test Runbook"
doc_family: "runbook"
owner_role: "ops"
---
# Test Runbook
## Purpose
This is a test.
""")

    registry = DocRegistry(str(docs_dir))
    registry.scan()
    linter = DocLintRunner(registry)
    results = linter.lint_all()
    assert len(results) == 1
    assert not results[0].passed
    assert any("missing_required_section: Success criteria" in issue for issue in results[0].issues)

def test_broken_link(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    test_doc = docs_dir / "overview.md"
    test_doc.write_text("""---
title: "Overview"
doc_family: "overview"
owner_role: "ops"
---
[Bad Link](nonexistent.md)
""")

    registry = DocRegistry(str(docs_dir))
    registry.scan()
    linter = DocLintRunner(registry)
    results = linter.lint_all()
    assert len(results) == 1
    assert not results[0].passed
    assert any("broken_local_link: nonexistent.md" in issue for issue in results[0].issues)
