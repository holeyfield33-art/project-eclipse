# Eclipse FastAPI Gateway (Development Security Foundation)

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
python -m pytest tests/ -v
```

## Security controls

- Production secret validation (production deployment remains unsupported)
- bcrypt + JWT auth
- Centralized RBAC
- New opaque tenant per registered account; real data-layer isolation remains unbuilt
- Process-local append-only audit hash chain
- Process-local rate limits on login/register
- Mass-assignment protection

See `../../docs/security-invariants.md` and `../../SECURITY_HARDENING_REPORT.md` for the bounded scope and open production work.
