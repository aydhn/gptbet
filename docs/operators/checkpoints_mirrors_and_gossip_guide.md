# Checkpoints, Mirrors, and Gossip

## Checkpoints
A checkpoint seals the log up to a specific tree size. It produces a `root_hash` that can be signed by multiple signers.

## Mirrors
A mirror independently tracks a log's checkpoints and verifies sync integrity. If it gets out of sync with what it expects or what gossip claims, it enters `quarantined` state.

## Gossip
A trust gossip envelope provides cross-plane notifications. When a signal is received, the local plane uses it to trigger a `verify_mirror_checkpoint` or `fetch_and_verify` rather than applying the state directly.
