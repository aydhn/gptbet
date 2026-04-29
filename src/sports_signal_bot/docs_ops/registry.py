import os
import yaml
import re
import datetime
from pathlib import Path
from .contracts import DocumentRecord, DocFamily, DocStatus, GlossaryTermRecord

class DocRegistry:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.documents: dict[str, DocumentRecord] = {}
        self.glossary: list[GlossaryTermRecord] = []

    def scan(self):
        self.documents.clear()
        if not self.docs_dir.exists():
            return

        for path in self.docs_dir.rglob("*.md"):
            try:
                record = self._parse_file(path)
                if record:
                    self.documents[record.doc_id] = record
            except Exception as e:
                pass # Ignore parsing errors for now

        self._load_glossary()

    def _parse_file(self, path: Path) -> DocumentRecord | None:
        content = path.read_text(encoding="utf-8")

        # very simple frontmatter extraction
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        metadata = {}
        if match:
            try:
                metadata = yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                pass

        doc_id = str(path.relative_to(self.docs_dir))

        last_updated = metadata.get("last_updated_at")
        if last_updated and isinstance(last_updated, str):
            try:
                last_updated = datetime.datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            except ValueError:
                last_updated = None

        last_reviewed = metadata.get("last_reviewed_at")
        if last_reviewed and isinstance(last_reviewed, str):
            try:
                last_reviewed = datetime.datetime.fromisoformat(last_reviewed.replace('Z', '+00:00'))
            except ValueError:
                last_reviewed = None

        family_str = metadata.get("doc_family", "overview")
        try:
             doc_family = DocFamily(family_str)
        except ValueError:
             doc_family = DocFamily.OVERVIEW

        status_str = metadata.get("status", "active")
        try:
             status = DocStatus(status_str)
        except ValueError:
             status = DocStatus.ACTIVE

        return DocumentRecord(
            doc_id=doc_id,
            title=metadata.get("title", path.stem.replace("_", " ").title()),
            doc_family=doc_family,
            path=str(path),
            owner_role=metadata.get("owner_role", "unowned"),
            owner_component=metadata.get("owner_component", "general"),
            intended_audience=metadata.get("intended_audience", []),
            status=status,
            last_updated_at=last_updated,
            last_reviewed_at=last_reviewed,
            freshness_window_days=metadata.get("freshness_window_days", 30),
            linked_docs=metadata.get("linked_docs", []),
            related_components=metadata.get("related_components", []),
            related_cli_commands=metadata.get("related_cli_commands", []),
            warnings=metadata.get("warnings", [])
        )

    def _load_glossary(self):
        glossary_path = self.docs_dir / "reference" / "glossary.md"
        if not glossary_path.exists():
            return

        content = glossary_path.read_text(encoding="utf-8")

        # Simple extraction logic: look for "### Term" or "- **Term**:"
        # For simplicity, let's just parse predefined terms if this logic is too complex
        # We'll keep it simple for this phase
        pass

    def get_document(self, doc_id: str) -> DocumentRecord | None:
        return self.documents.get(doc_id)

    def list_documents(self) -> list[DocumentRecord]:
        return list(self.documents.values())
