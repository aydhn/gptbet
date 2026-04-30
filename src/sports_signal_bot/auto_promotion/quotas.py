from .contracts import ProgressionQuotaRecord

class QuotaManager:
    def __init__(self, config: dict):
        qconf = config.get("quotas", {})
        self.quota = ProgressionQuotaRecord(
            max_progressions=qconf.get("max_auto_progressions_per_run", 10),
            max_kills=qconf.get("max_auto_kills_per_run", 5)
        )

    def can_progress(self) -> bool:
        return self.quota.used_progressions < self.quota.max_progressions

    def can_kill(self) -> bool:
        return self.quota.used_kills < self.quota.max_kills

    def record_progression(self):
        self.quota.used_progressions += 1

    def record_kill(self):
        self.quota.used_kills += 1
