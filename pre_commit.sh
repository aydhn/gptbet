#!/bin/bash
echo "Running pre-commit checks..."
python -m pytest tests/remediation_lanes/ tests/verifier_portal/
