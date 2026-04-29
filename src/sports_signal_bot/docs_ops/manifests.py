import datetime
from .registry import DocRegistry
from .freshness import FreshnessReporter
from .lint import DocLintRunner
from .coverage import DocCoverageChecker
from .contracts import DocsOpsManifestRecord, DocFamily

class ManifestGenerator:
    def __init__(self, registry: DocRegistry):
        self.registry = registry
        self.freshness = FreshnessReporter(registry)
        self.lint = DocLintRunner(registry)
        self.coverage = DocCoverageChecker(registry)

    def generate(self) -> DocsOpsManifestRecord:
        docs = self.registry.list_documents()
        total_docs = len(docs)

        family_counts = {f.value: 0 for f in DocFamily}
        for d in docs:
            family_counts[d.doc_family.value] = family_counts.get(d.doc_family.value, 0) + 1

        stale_count = sum(1 for r in self.freshness.check_all() if r.is_stale)

        coverage_results = self.coverage.check_coverage()
        missing_coverage = [r.component for r in coverage_results if r.coverage_score < 0.6]

        lint_results = self.lint.lint_all()
        total_lint_issues = sum(len(r.issues) for r in lint_results)

        return DocsOpsManifestRecord(
            total_docs_count=total_docs,
            docs_by_family=family_counts,
            stale_docs_count=stale_count,
            missing_coverage_components=missing_coverage,
            total_lint_issues=total_lint_issues,
            critical_runbooks_count=family_counts[DocFamily.RUNBOOK.value],
            incident_playbooks_count=family_counts[DocFamily.INCIDENT_PLAYBOOK.value],
            generated_at=datetime.datetime.now(datetime.timezone.utc)
        )
