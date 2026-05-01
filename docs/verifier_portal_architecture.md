# Verifier Portal Architecture

## Overview
This phase introduces the Verifier Portal Experience to the system, acting as a controlled external consumer layer. It bridges the gap between the public verification gateway and third-party verifiers, offering a specialized experience tailored to the verifier's audience profile.

## Core Concepts
- **Profile-Aware Views**: Distinct audience profiles (e.g., `public_viewer`, `external_auditor`) determine access level, proof depth, and visible details.
- **Verification View Packets**: Structured read-only snapshots containing source data with relevant caveats and redactions.
- **Challenge Intake API**: Controlled endpoints for submitting challenges with built-in validation, deduplication, and quarantine mechanisms.
- **Notarized Disclosures**: Artifacts equipped with a signed delivery summary containing references to proof logic and verified receipts.
- **Dashboard Feeds**: Observability feeds providing an active, structured summary of publications, check-points, and readiness status.
- **Consistency and Freshness**: Enforces strict labeling of data freshness, marking stale feeds with warnings to prevent misinterpretation.

## Audience Profiles
- `public_viewer`
- `registered_verifier`
- `trusted_external_verifier`
- `external_auditor`
- `quarantine_reviewer`
- `internal_preview_viewer`

## Read-Only Philosophy
The Portal is purely for viewing and verifying content. It strictly disallows active state mutations directly via the API. External modifications must flow through challenge intakes and undergo internal adjudication.
