import pytest
from sports_signal_bot.docs_ops.registry import DocRegistry
from sports_signal_bot.docs_ops.coverage import DocCoverageChecker

def test_doc_coverage(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    test_doc = docs_dir / "inference_runbook.md"
    test_doc.write_text("""---
title: "Inference Runbook"
doc_family: "runbook"
owner_role: "ops"
owner_component: "inference"
---
# Inference Runbook
""")

    registry = DocRegistry(str(docs_dir))
    registry.scan()
    checker = DocCoverageChecker(registry)
    # mock critical components to just inference for testing
    checker.critical_components = ["inference"]
    results = checker.check_coverage()

    assert len(results) == 1
    assert results[0].component == "inference"
    assert results[0].has_runbook
    assert not results[0].has_playbook
    assert results[0].coverage_score > 0
