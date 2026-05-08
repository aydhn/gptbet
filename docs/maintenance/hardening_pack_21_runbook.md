# Hardening Pack 21 Runbook

Run the following commands to assess Terminal Lifecycle Hardening:

```bash
# Run the full pack
python -m sports_signal_bot.main terminal-lifecycle-hardening run-hardening-pack-21

# Preview Health
python -m sports_signal_bot.main terminal-lifecycle-hardening preview-terminal-lifecycle-health

# List Strategies
python -m sports_signal_bot.main terminal-lifecycle-hardening list-terminal-lifecycle-strategies
```

Review artifacts (JSON files generated in the root directory) and ensure no critical warnings appear concerning ownership gaps or missing visibility sections.
