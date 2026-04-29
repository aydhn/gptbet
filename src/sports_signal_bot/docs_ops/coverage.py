from .registry import DocRegistry
from .contracts import DocCoverageRecord, DocFamily
import yaml

class DocCoverageChecker:
    def __init__(self, registry: DocRegistry):
        self.registry = registry
        self.critical_components = self._load_components()

    def _load_components(self) -> list[str]:
        try:
            with open("configs/docs/coverage.yaml", "r") as f:
                config = yaml.safe_load(f)
                return config.get("critical_component_doc_coverage_rules", [])
        except Exception:
             return ["inference", "monitoring", "scheduler", "release"]

    def check_coverage(self) -> list[DocCoverageRecord]:
        results = []

        # group docs by component
        comp_docs = {comp: [] for comp in self.critical_components}
        for doc in self.registry.list_documents():
            comp = doc.owner_component
            if comp in comp_docs:
                comp_docs[comp].append(doc)
            for related in doc.related_components:
                if related in comp_docs:
                    comp_docs[related].append(doc)

        for comp, docs in comp_docs.items():
            has_overview = any(d.doc_family == DocFamily.OVERVIEW for d in docs)
            has_runbook = any(d.doc_family == DocFamily.RUNBOOK for d in docs)
            has_playbook = any(d.doc_family == DocFamily.INCIDENT_PLAYBOOK for d in docs)
            has_op_ref = any(d.doc_family == DocFamily.OPERATOR for d in docs)
            has_cli_ref = any(d.doc_family == DocFamily.REFERENCE and "cli" in d.title.lower() for d in docs)

            score = sum([has_overview, has_runbook, has_playbook, has_op_ref, has_cli_ref]) / 5.0

            results.append(DocCoverageRecord(
                component=comp,
                has_overview=has_overview,
                has_runbook=has_runbook,
                has_playbook=has_playbook,
                has_operator_reference=has_op_ref,
                has_cli_reference=has_cli_ref,
                coverage_score=score
            ))

        return results
