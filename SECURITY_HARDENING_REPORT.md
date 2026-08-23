# Security Hardening Report — Project Eclipse

**Directive:** SECURITY HARDENING DIRECTIVE v1  
**Repository:** holeyfield33-art/project-eclipse  
**Status:** Implementation complete; 49/49 security tests passed locally

## Summary

Security foundation implemented on the existing scaffold without architecture redesign or product feature creep.

### P0 CLOSED
- Authentication (bcrypt + JWT, expire, inactive, invalid signature)
- RBAC (centralized permissions + alert action matrix)
- Tenant isolation (tenant_id on entities/alerts/cases/audit)
- Secrets fail-closed in production
- Alert action authorization + audit on every action
- Append-only audit with SHA-256 hash chain + verification

### P1 CLOSED
- Entity privacy boundary documented; hashes vs display names
- IDOR/BOLA tests on entity/alert/case endpoints
- Input validation (limits, enums, extra=forbid mass assignment)
- Rate limiting on /login and /register
- CORS explicit origins; docs toggle via ENABLE_DOCS
- ML terminology: `feature_contributions` (not SHAP); baseline documented honestly

### P0 OPEN
- None for the in-memory security foundation scope

### P1 OPEN / Known limitations
- Persistence still in-memory for the security foundation (Postgres schema hardened with tenant_id + audit columns; SQLAlchemy wiring is later phase)
- Injection regression tests deferred until real DB query layer is implemented (parameterized queries required then)
- Audit chain is application-level tamper evidence, not WORM/crypto immutability
- Redis/ES/Kafka production auth documented but not enforced in local compose (by design)

### Tests executed
```
PYTHONPATH=. pytest tests/security/ -v
49 passed
```

### Dependency changes
- Added: pytest, pytest-asyncio, email-validator (via pydantic[email])
- Constrained bcrypt <4.1 for passlib compatibility
- No heavyweight new frameworks

### Key files
- `app/core/config.py`, `security.py`, `rbac.py`
- `app/api/deps.py`
- `app/services/audit.py`, `store.py`, `rate_limit.py`
- `tests/security/*`
- `docs/security-invariants.md`, `docs/entity-privacy.md`
- `data/schemas/postgres/001_init.sql` (tenant_id + audit hash columns)

### Release rule
P0 OPEN = 0 for implemented security boundary.  
No Phase 1 pilot until real data layer inherits the same tenant/auth/audit invariants.
