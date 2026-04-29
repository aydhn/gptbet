import re
from pathlib import Path
from .registry import DocRegistry
from .contracts import DocLintResultRecord, DocFamily

class DocLintRunner:
    def __init__(self, registry: DocRegistry):
        self.registry = registry

    def lint_all(self) -> list[DocLintResultRecord]:
        results = []
        for doc in self.registry.list_documents():
            results.append(self.lint_document(doc))
        return results

    def lint_document(self, doc) -> DocLintResultRecord:
        issues = []

        if doc.owner_role == "unowned":
            issues.append("missing_owner_metadata")

        path = Path(doc.path)
        if not path.exists():
            issues.append("file_not_found")
            return DocLintResultRecord(doc_id=doc.doc_id, path=doc.path, issues=issues, passed=False)

        content = path.read_text(encoding="utf-8")

        if doc.doc_family == DocFamily.RUNBOOK:
            # required sections
            required_sections = ["Purpose", "When to use", "Preconditions", "Inputs needed",
                                 "Step-by-step actions", "Success criteria", "Failure branches",
                                 "Escalation path"]
            for section in required_sections:
                if not re.search(r"^#+\s+" + re.escape(section), content, re.IGNORECASE | re.MULTILINE):
                    issues.append(f"missing_required_section: {section}")

        elif doc.doc_family == DocFamily.INCIDENT_PLAYBOOK:
            required_sections = ["Symptom summary", "Severity guidance", "First 5 minutes",
                                 "Escalation thresholds"]
            for section in required_sections:
                if not re.search(r"^#+\s+" + re.escape(section), content, re.IGNORECASE | re.MULTILINE):
                    issues.append(f"missing_required_section: {section}")

        # Check broken links
        links = re.findall(r"\]\((.*?\.md)\)", content)
        for link in links:
            if link.startswith("http"):
                continue
            # basic local link check
            target = path.parent / link
            if not target.resolve().exists():
                issues.append(f"broken_local_link: {link}")

        return DocLintResultRecord(
            doc_id=doc.doc_id,
            path=doc.path,
            issues=issues,
            passed=len(issues) == 0
        )
