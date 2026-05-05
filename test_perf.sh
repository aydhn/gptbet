#!/bin/bash
set -e
export PYTHONPATH=src

python -m sports_signal_bot.main performance-hardening run-hardening-pack-02
python -m sports_signal_bot.main performance-hardening preview-performance-envelope-report
python -m sports_signal_bot.main performance-hardening preview-load-profile-report
python -m sports_signal_bot.main performance-hardening preview-hot-path-report
python -m sports_signal_bot.main performance-hardening preview-cache-discipline-report
python -m sports_signal_bot.main performance-hardening preview-perf-regression-report
python -m sports_signal_bot.main performance-hardening preview-performance-hardening-health
python -m sports_signal_bot.main performance-hardening list-performance-hardening-strategies

echo "All commands passed!"
