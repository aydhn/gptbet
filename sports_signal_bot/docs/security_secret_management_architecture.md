# Security & Secret Management Architecture

## Local-First Security
Although the system operates locally, rigorous security hygiene is maintained:
- **Redaction**: All logs, manifests, and CLI previews are redacted.
- **Config Layering**: Config precedence is strictly defined and verifiable.
- **Fail-Safe**: Missing secrets trigger fallback to dry-run mode rather than failing open.
- **Least-Privilege**: Various execution modes enforce allowed commands and behaviors.

## Trust Boundaries
- Execution contexts like `run-inference` operate with restricted side-effects.
- External routing (e.g., dispatch) verifies outbound targets against `EndpointAllowlist`.
- Local writes enforce `FilesystemAllowlist` boundaries.

## Architecture
- `RedactionEngine`: Scrubs nested payloads of sensitive fields.
- `SecretResolver`: Traces and validates secret definitions.
- `CommandSafetyGate`: Enforces confirmation for high-risk CLI interactions.
- `SecurityAuditRunner`: Evaluates runtime integrity.

## Commands
```bash
python -m sports_signal_bot.main security run-security-audit
python -m sports_signal_bot.main security preview-effective-config
python -m sports_signal_bot.main security check-runtime-privileges
```
