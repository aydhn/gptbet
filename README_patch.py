import re

with open("README.md", "r") as f:
    content = f.read()

patch = """
## Post-100 Hardening Pack 18
**Goal:** Continuity arbitration rails, scheduler recovery fabrics, archive proof meshes and worldwide visibility ledgers.
**Why it matters:** Arbitration honesty ensures that continuity ambiguity, proof staleness, and visibility suppressions are transparently ledged without overriding local sovereignty. Proof meshes and visibility ledgers act as critical safety features ensuring non-repudiation of recovery steps and preventing hidden continuity gaps.

### Commands:
- `python -m sports_signal_bot.main continuity-arbitration-hardening run-hardening-pack-18`
- `python -m sports_signal_bot.main continuity-arbitration-hardening preview-continuity-arbitration-rail-report`
- `python -m sports_signal_bot.main continuity-arbitration-hardening preview-scheduler-recovery-fabric-report`
- `python -m sports_signal_bot.main continuity-arbitration-hardening preview-archive-proof-mesh-report`
- `python -m sports_signal_bot.main continuity-arbitration-hardening preview-worldwide-visibility-ledger-report`
- `python -m sports_signal_bot.main continuity-arbitration-hardening preview-continuity-arbitration-health`
"""

if "Post-100 Hardening Pack 18" not in content:
    content += patch

with open("README.md", "w") as f:
    f.write(content)
