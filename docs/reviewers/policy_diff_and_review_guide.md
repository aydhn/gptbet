# Policy Diff and Review Guide

## Review Workflow
- Inspect the diff: Look closely at removed rules (they relax constraints) and modified conditions.
- Safety: Check if `require_approval` actions were circumvented or precedence was manipulated.

## Pre-promotion Requirements
- Compatibility pass
- Evaluation simulation / replay to check unintended behaviors
