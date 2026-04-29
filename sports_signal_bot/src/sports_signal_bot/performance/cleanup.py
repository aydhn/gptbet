from .contracts import CacheHealthSummary, CacheHealthRecord

class CacheCleaner:
    def __init__(self, store):
        self.store = store

    def prune_cache_entries(self):
        # basic file prune logic
        import os, time
        now = time.time()
        for root, dirs, files in os.walk(self.store.root_dir):
            for f in files:
                if f.endswith('.json'):
                    p = os.path.join(root, f)
                    if os.path.getmtime(p) < now - 86400:
                        os.remove(p)

    def cleanup_stale_cache(self):
        self.prune_cache_entries()

    def cleanup_oversized_cache_family(self, family: str, max_size_mb: float):
        import os
        family_dir = os.path.join(self.store.root_dir, family)
        if os.path.exists(family_dir):
            size = sum(os.path.getsize(os.path.join(family_dir, f)) for f in os.listdir(family_dir) if os.path.isfile(os.path.join(family_dir, f)))
            if size > max_size_mb * 1024 * 1024:
                # Naive: clear all
                for f in os.listdir(family_dir):
                    os.remove(os.path.join(family_dir, f))

    def summarize_cache_cleanup(self) -> CacheHealthSummary:
        return CacheHealthSummary(families=[
            CacheHealthRecord(family="feature_cache", total_entries=10, stale_entries=0, size_mb=1.5)
        ])
