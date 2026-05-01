# Compliance Pipeline & Drift Guide

Operators use the continuous verification pipeline to assert the health of the deployment.
Drifts are classified by severity (e.g., tolerated vs. critical) and can block releases.

Use `python -m sports_signal_bot.main conformance run-conformance-pass` to verify current state manually.
