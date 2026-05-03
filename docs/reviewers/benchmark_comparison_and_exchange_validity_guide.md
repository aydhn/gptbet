# Benchmark Comparison & Exchange Validity Guide

## Benchmark Comparisons
Treaties are compared against baselines.
- Focus on `missing_dimension` and `weaker_than_baseline`.
- Note: Weaker than baseline does not mean invalid, but it should prompt a review.

## Exchange Validity
- Attestation exchange packets are constantly watched for validity.
- If an underlying attestation expires or a treaty is superseded, the exchange packet status will downgrade (e.g., `exchanged_invalidated`).
