import uuid
from datetime import datetime
from typing import Dict, List, Optional

from .contracts import (
    KnowledgeEntryRecord,
    KnowledgeEntryStatus,
    KnowledgeScopeRecord,
    MemoryType,
)


class KnowledgeMemoryStore:
    def __init__(self):
        self.entries: Dict[str, KnowledgeEntryRecord] = {}

    def add_entry(self, entry: KnowledgeEntryRecord) -> None:
        self.entries[entry.entry_id] = entry

    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntryRecord]:
        return self.entries.get(entry_id)

    def find_entries(
        self, memory_type: Optional[MemoryType] = None, active_only: bool = True
    ) -> List[KnowledgeEntryRecord]:
        results = []
        for e in self.entries.values():
            if active_only and e.status != KnowledgeEntryStatus.active:
                continue
            if memory_type and e.memory_type != memory_type:
                continue

            # check expiry
            if e.expiry and e.expiry < datetime.utcnow():
                e.status = KnowledgeEntryStatus.expired
                continue

            results.append(e)
        return results

    def deprecate_entry(self, entry_id: str) -> bool:
        if entry_id in self.entries:
            self.entries[entry_id].status = KnowledgeEntryStatus.deprecated
            return True
        return False
