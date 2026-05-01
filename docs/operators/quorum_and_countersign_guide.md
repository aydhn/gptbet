# Quorum and Countersign Guide

As an operator, understanding the thresholds for progressing changes is key:
- Check the required group logic (`mandatory_signer_groups`) in your target configuration.
- Evaluate the collective `weighted_trust_total` against the `min_weighted_trust`.
- If an action fails quorum despite multiple signers, check for missing mandatory signers or vetoes.
