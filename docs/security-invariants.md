# Eclipse Security Invariants

Non-negotiable properties of the security foundation. Each invariant is enforced
in code and covered by automated tests under `backend/api/tests/security/`.

| ID | Invariant | Primary tests |
|----|-----------|---------------|
| I-001 | Anonymous users cannot access protected resources | `test_authentication.py` |
| I-002 | Users cannot access another tenant's resources | `test_tenant_isolation.py`, `test_idor.py` |
| I-003 | Clients cannot assign themselves privileges | `test_authentication.py`, `test_mass_assignment.py` |
| I-004 | Clients cannot forge audit actors | `test_audit_integrity.py` |
| I-005 | Audit records cannot be modified through the application | `test_audit_integrity.py` |
| I-006 | Production cannot start with development secrets | `test_secret_configuration.py` |
| I-007 | Raw sensitive identifiers are never emitted in logs/audit details | `audit.py` sanitizer; `docs/entity-privacy.md` |
| I-008 | Risk scores cannot be client-controlled | Server-computed only |
| I-009 | Authorization is checked server-side | `deps.py` + RBAC matrix tests |
| I-010 | Every privileged action produces an audit event | `test_audit_integrity.py` |

## Audit integrity guarantee (honest scope)

- Application layer: no update/delete endpoints; actor_id and timestamps server-generated.
- Tamper evidence: per-tenant SHA-256 hash chain detects modified/deleted/reordered/inserted events.
- NOT claimed: cryptographic immutability or WORM storage. Pair with DB INSERT-only grants and log shipping in production.

## Alert action matrix

| Action | analyst | manager | admin | auditor |
|--------|---------|---------|-------|---------|
| flag | yes | yes | yes | no |
| escalate | yes | yes | yes | no |
| dismiss | no | yes | yes | no |
| freeze | no | yes | yes | no |
| report | no | yes | yes | no |

Encoded in `app.core.rbac.ALERT_ACTION_PERMISSIONS`.
