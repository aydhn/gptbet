# Operator Guide: Final Convergence and Terminal Acceptance

This guide is for operators handling the final convergence and acceptance process.

## Running Final Convergence

Use the CLI to run the final convergence pass:

```bash
python -m sports_signal_bot.main run-hardening-pack-20
```

You can specify a strategy:

```bash
python -m sports_signal_bot.main run-hardening-pack-20 --strategy balanced
```

## Reviewing Artifacts

After running the pass, several artifacts are generated:

*   `final_hardening_convergence.json`
*   `frozen_baselines.json`
*   `production_readiness_review_surfaces.json`
*   `terminal_acceptance_packs.json`
*   `final_convergence_matrix.json`

Use the preview commands to inspect them:

```bash
python -m sports_signal_bot.main preview-final-convergence-report
python -m sports_signal_bot.main preview-frozen-baseline-report
python -m sports_signal_bot.main preview-readiness-review-report
python -m sports_signal_bot.main preview-terminal-acceptance-report
python -m sports_signal_bot.main preview-final-convergence-health
```
