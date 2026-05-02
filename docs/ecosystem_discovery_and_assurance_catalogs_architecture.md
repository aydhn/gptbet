# Ecosystem Discovery and Assurance Catalogs Architecture

## Overview
This architecture sits on top of the assurance federation layer to provide public assurance registry catalogs, auto-negotiated verifier protocol profiles, and portable proof marketplaces-style indexing.

## Core Concepts
1. **Discovery is not Trust**: Just because a catalog or registry is discovered does not mean it is trusted. Trust is policy-driven.
2. **Auto-Negotiated Verifier Protocols**: Clients and verifiers negotiate a safe, common subset of capabilities.
3. **Freshness & Supersession**: Catalogs track freshness, and stale or superseded entries are suppressed or downgraded.
4. **Quarantine**: Unknown or unsafe discoveries are quarantined by default until reviewed.
