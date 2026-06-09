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
        metadata = self._extract_metadata(content)

        return DocumentRecord(
            doc_id=str(path.relative_to(self.docs_dir)),
            title=metadata.get("title", path.stem.replace("_", " ").title()),
            doc_family=self._parse_doc_family(metadata.get("doc_family", "overview")),
            path=str(path),
            owner_role=metadata.get("owner_role", "unowned"),
            owner_component=metadata.get("owner_component", "general"),
            intended_audience=metadata.get("intended_audience", []),
            status=self._parse_doc_status(metadata.get("status", "active")),
            last_updated_at=self._parse_datetime(metadata.get("last_updated_at")),
            last_reviewed_at=self._parse_datetime(metadata.get("last_reviewed_at")),
            freshness_window_days=metadata.get("freshness_window_days", 30),
            linked_docs=metadata.get("linked_docs", []),
            related_components=metadata.get("related_components", []),
            related_cli_commands=metadata.get("related_cli_commands", []),
            warnings=metadata.get("warnings", [])
        )

    def _extract_metadata(self, content: str) -> dict:
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                pass
        return {}

    def _parse_datetime(self, date_val) -> datetime.datetime | None:
        if date_val and isinstance(date_val, str):
            try:
                return datetime.datetime.fromisoformat(date_val.replace('Z', '+00:00'))
            except ValueError:
                return None
        return date_val if isinstance(date_val, datetime.datetime) else None

    def _parse_doc_family(self, family_str: str) -> DocFamily:
        try:
            return DocFamily(family_str)
        except ValueError:
            return DocFamily.OVERVIEW

    def _parse_doc_status(self, status_str: str) -> DocStatus:
        try:
            return DocStatus(status_str)
        except ValueError:
            return DocStatus.ACTIVE

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
