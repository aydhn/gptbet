---
title: Provider Registry Reference
owner: Data Platform Engineer
family: reference
freshness_window: 90
---

# Provider Registry Reference

This reference lists the supported provider kinds and standard capabilities.

## Provider Kinds
- `REMOTE_JSON_API`
- `LOCAL_FILE_FEED`
- `NORMALIZED_SNAPSHOT_STORE`
- `CACHED_PROXY`
- `MANUAL_DROPZONE`
- `STUB_TEST_PROVIDER`

## Capability Matrix
Capabilities are strictly enforced. A provider will not be routed a request for `fixtures` if it only supports `odds_snapshots`.
