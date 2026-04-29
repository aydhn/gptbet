---
title: "Glossary"
doc_family: "reference"
owner_role: "operations_team"
owner_component: "general"
status: "active"
---

# Glossary

- **run_id:** A unique identifier for a specific execution trace.
- **slot:** A logical time window (morning, midday, evening) grouping operations.
- **canary:** A candidate model running in parallel to stable, but not dispatching signals.
- **freeze:** A state where automated dispatches are blocked due to critical health failures.
- **degrade:** A state where non-critical operations (like canary evaluation) are skipped to ensure stability.
- **review queue:** A list of signals requiring manual operator approval before dispatch.
