import re

def fix_file(path, replacements):
    with open(path, "r") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)

fix_file("sports_signal_bot/src/sports_signal_bot/source_selection/catalog.py", [
    ("entries: List[SourceCatalogEntry] = None", "entries: Optional[List[SourceCatalogEntry]] = None")
])

fix_file("sports_signal_bot/src/sports_signal_bot/source_selection/scoring.py", [
    ("weights: Dict[str, float] = None", "weights: Optional[Dict[str, float]] = None"),
    ("active_regimes: List[str] = None", "active_regimes: Optional[List[str]] = None")
])

fix_file("sports_signal_bot/src/sports_signal_bot/source_selection/policies.py", [
    ("families = {}", "families: Dict[str, List[SourceEligibilityRecord]] = {}")
])

fix_file("sports_signal_bot/src/sports_signal_bot/source_selection/diagnostics.py", [
    ("exclusion_counts = defaultdict(int)", "exclusion_counts: Dict[str, int] = defaultdict(int)"),
    ("family_totals = defaultdict(int)", "family_totals: Dict[str, int] = defaultdict(int)"),
    ("family_eligible = defaultdict(int)", "family_eligible: Dict[str, int] = defaultdict(int)")
])

fix_file("sports_signal_bot/src/sports_signal_bot/source_selection/chain.py", [
    ("self.policies = []", "self.policies: List[Any] = []")
])

fix_file("sports_signal_bot/src/sports_signal_bot/source_selection/runner.py", [
    ("active_regimes: List[str] = None", "active_regimes: Optional[List[str]] = None")
])
