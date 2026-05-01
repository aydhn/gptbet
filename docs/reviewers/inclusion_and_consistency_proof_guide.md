# Inclusion and Consistency Proofs

Proofs are the mathematical guarantee of transparency.

- **Inclusion Proofs**: Prove that a specific `event_hash` is a leaf in the tree leading to a given `root_hash`.
- **Consistency Proofs**: Prove that an old `root_hash` is a prefix of a new `root_hash`.

Verifiers should fail securely if proofs are missing or invalid, ensuring tampering is evident.
