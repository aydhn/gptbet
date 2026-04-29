import re
from pathlib import Path

def patch_doc(path_str):
    p = Path(path_str)
    if not p.exists():
        return
    content = p.read_text(encoding="utf-8")
    if not content.startswith("---"):
        frontmatter = f"""---
title: "{p.stem.replace('_', ' ').title()}"
doc_family: "overview"
owner_role: "engineering_team"
owner_component: "general"
status: "active"
---

"""
        p.write_text(frontmatter + content, encoding="utf-8")

patch_doc("docs/scheduled_orchestration_architecture.md")
patch_doc("docs/release_promotion_architecture.md")
