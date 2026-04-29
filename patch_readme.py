with open('sports_signal_bot/README.md', 'r') as f:
    content = f.read()

if "## Security and Secret Management" not in content:
    content += """
## Security and Secret Management
The security layer isolates secret resolution, enforces redaction for sensitive payloads, and restricts access via least-privilege profiles.
- Never commit real tokens to `.env` or `.yaml` files.
- Use `.env.local` for local secrets.
- Redaction and config hygiene can be validated using the `security run-security-audit` CLI command.
"""

with open('sports_signal_bot/README.md', 'w') as f:
    f.write(content)
