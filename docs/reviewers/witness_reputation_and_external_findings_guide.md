# Witness Reputation and External Findings Guide

This guide outlines how to interpret and manage the reputation of external witnesses and the findings they produce.

## Witness Reputation

Reputation scores range from 0 to 100 and determine the trust level of an external responder.

- **Signals**: Reputation is built on signals like `correct_confirmation`, `false_alarm`, and `timely_response`.
- **Adjustments**: Explicit adjustments can be applied (e.g., penalties for unsupported challenges, credits for high-value anomaly confirmations).
- **Bands**: Scores map to bands: `excellent` (>80), `strong` (>60), `adequate` (default), `low_trust` (<30).

**Reviewer Action**: If a witness's reputation drops to `low_trust` or exhibits instability (frequent downgrades), their findings should be treated with extreme skepticism and manually reviewed.

## External Findings

External findings arrive with varying severities (`info`, `warning`, `error`, `critical`).

- **Local Mapping**: The system automatically suggests local actions based on finding severity and witness reputation.
- **Verification**: A finding is *never* accepted as absolute truth. It serves as an input to the local anomaly or review case process.

**Reviewer Action**: Review findings marked for 'open_review_case' or 'open_anomaly_case'. Decide whether to accept the finding as supporting evidence or reject it.
