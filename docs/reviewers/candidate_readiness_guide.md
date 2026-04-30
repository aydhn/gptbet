---
owner: qa_team
family: guide
freshness: 30d
---

# Candidate Readiness Guide

## Overview
This guide explains the Candidate Readiness bands and what they signify for reviewers.

## Readiness Bands
- **not_ready**: Candidate has failed or has not completed required stages.
- **conditionally_ready**: Candidate has passed gates but requires explicit approval (often due to higher risk).
- **review_ready**: Candidate is ready for manual review.
- **approval_ready**: Candidate is ready for final sign-off.
- **release_candidate_ready**: Candidate has passed all required automated checks and approvals, and is ready for the `promote_or_kill` decision.
- **blocked_not_ready**: Candidate explicitly failed a safety check or gating requirement and is blocked from proceeding.

## Actioning
Reviewers should focus on `conditionally_ready` and `review_ready` candidates in the `Standard` or `High-Risk` lanes. `Fast Lane` candidates typically reach `release_candidate_ready` without heavy manual intervention if they meet strict scoping rules.
