---
title: "FAQ"
doc_family: "reference"
owner_role: "operations_team"
owner_component: "general"
status: "active"
---

# FAQ

**Q: If freeze is active, what do I do?**
A: Do not force release immediately. Read the alarm, consult the `docs/incidents/monitoring_health_drop.md` playbook, and triage the root cause.

**Q: What is the difference between dry-run and real dispatch?**
A: A dry-run executes the entire inference chain but prints the final payload to the console instead of routing it to Telegram.
