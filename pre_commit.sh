#!/bin/bash
echo "Running pre-commit checks..."
python -m pytest tests/verifier_portal/
