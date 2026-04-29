# Secret Handling Guide

## Do Not Commit Secrets
Never commit real tokens into tracked `.env` or `.yaml` files.

Use `.env.local` for local overrides, which is gitignored. The `.env.example` should contain only placeholders.

## Configuration Precedence
1. Environment Variables
2. `.env.local`
3. Repository Defaults

## Troubleshooting
If a command blocks, check:
- Is `--confirm` required?
- Is the correct `SECURITY_PROFILE` set?
