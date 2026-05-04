# Operators Guide: Governance Health Compilation

## Running Passes
Use `python -m sports_signal_bot.main run-governance-health-pass` to execute portfolio sorting, replay routing, convergence updating, and health compilation.

## Previews
- `preview-stabilization-portfolios`
- `preview-lineage-replay-fabrics`
- `preview-successor-convergence-registries`
- `preview-governance-health-compilers`
- `preview-governance-health`

## What to Watch For
- **Replay Pressure**: If the fabric is backpressured, replays are failing to keep up, and health will degrade to `review_only`.
- **Convergence Debt**: Weak convergence blocks successor progression.
- **Sovereignty Pass Failures**: A failed sovereignty pass drops the compiled band to `critically_fragile`.
