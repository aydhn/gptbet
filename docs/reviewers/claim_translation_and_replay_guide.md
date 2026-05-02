# Claim Translation and Replay Guide

Reviewers are responsible for auditing translation safety.

- **Semantic Loss Risk**: If a translation maps a strong claim to a weak one, caveats must be added.
- **Replay Mismatches**: A replay mismatch means the external registry trusted a packet that the local policy rejects. This indicates policy drift.
