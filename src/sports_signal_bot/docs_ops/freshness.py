import datetime
from .registry import DocRegistry
from .contracts import DocFreshnessRecord

class FreshnessReporter:
    def __init__(self, registry: DocRegistry):
        self.registry = registry

    def check_all(self) -> list[DocFreshnessRecord]:
        now = datetime.datetime.now(datetime.timezone.utc)
        results = []

        for doc in self.registry.list_documents():
            last_reviewed = doc.last_reviewed_at or doc.last_updated_at
            if last_reviewed:
                # Ensure last_reviewed is timezone aware for comparison
                if last_reviewed.tzinfo is None:
                    last_reviewed = last_reviewed.replace(tzinfo=datetime.timezone.utc)
                delta = now - last_reviewed
                days = delta.days
                is_stale = days > doc.freshness_window_days
                days_overdue = days - doc.freshness_window_days if is_stale else 0
            else:
                days = None
                is_stale = True
                days_overdue = None

            results.append(DocFreshnessRecord(
                doc_id=doc.doc_id,
                is_stale=is_stale,
                days_since_review=days,
                days_overdue=days_overdue,
                owner_role=doc.owner_role,
                owner_component=doc.owner_component
            ))

        return results
