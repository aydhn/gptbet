# Schema Governance Architecture

## Purpose
As the ML infrastructure scales with multiple decoupled layers (features, calibration, stacker, release, inference), the risk of schema breaking changes between producer and consumer components rises exponentially. The Schema Governance layer provides safety boundaries.

## Versioning Model
Every schema contract specifies:
- `major_version`: Breaking changes.
- `minor_version`: Backward-compatible extensions.
- `patch_version`: Semantic fixes.
Combined into `vX.Y.Z`.

## Compatibility Taxonomy
Compatibility classifications:
- `fully_compatible`
- `backward_compatible`
- `forward_compatible_with_warnings`
- `migration_required`
- `incompatible_breaking`

## Manifest Envelope Standard
All manifests are wrapped in a standardized envelope specifying `manifest_family`, `schema_version`, `producer_component`, `artifact_id`, and `payload` to unify processing and tracing.

## Migration and Adapter Philosophy
Artifact resolvers utilize a `VersionedLoader`. Instead of forcing a massive retroactive migration script, legacy or older artifacts are loaded via read-old-write-new logic through `ManifestShim` and `ContractAdapter`.

## Deprecation Policy
Fields can be flagged as deprecated without immediate removal. Overusing deprecated fields emits `DeprecationNoticeRecord` items that surface in monitoring.

## Future Path
This is a foundational layer capable of connecting to external Schema Registries or supporting advanced cryptographically-signed manifests in the future.
