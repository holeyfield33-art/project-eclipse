# Eclipse FastAPI Gateway (Security Foundation)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Tests

```bash
cd backend/api
pip install -r requirements.txt
PYTHONPATH=. pytest tests/security/ -v
```

## Security controls

- Fail-closed production secrets
- bcrypt + JWT auth
- Centralized RBAC
- Tenant isolation
- Append-only audit with hash chain
- Rate limits on login/register
- Mass-assignment protection

See `docs/security-invariants.md`.
