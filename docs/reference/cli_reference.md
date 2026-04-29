---
title: "CLI Reference"
doc_family: "reference"
owner_role: "engineering_team"
owner_component: "general"
status: "active"
---

# CLI Reference

## Core Commands

### `run-slot`
Executes the inference and dispatch chain for a given slot.
- **Usage:** `python -m sports_signal_bot.main run-slot --slot midday`
- **Safe usage:** Append `--dry-run` to avoid sending real messages.

### `run-refresh`
Triggers the data ingestion and artifact generation process.
- **Usage:** `python -m sports_signal_bot.main run-refresh`

### `preview-docs-index`
Previews the documentation registry and freshness state.
- **Usage:** `python -m sports_signal_bot.main docs preview-index`

### `run-docs-lint`
Lints documentation for broken links and missing sections.
- **Usage:** `python -m sports_signal_bot.main docs lint`
