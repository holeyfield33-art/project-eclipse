# Eclipse API Reference (v1)

Base URL: `/api/v1`

Interactive docs available at `/docs` (Swagger) when the FastAPI service is running.

## Authentication

- `POST /auth/login` – email + password → JWT
- `POST /auth/register` – create user (admin-gated in production)

JWT carries role claims: `analyst` | `manager` | `admin` | `auditor`.

## Entities

- `GET /entities?q=` – search
- `GET /entities/{id}` – profile + risk score + SHAP
- `GET /entities/{id}/network?depth=` – graph neighborhood
- `GET /entities/{id}/transactions` – history

## Alerts

- `GET /alerts` – live feed (filter by severity, status)
- `GET /alerts/overview` – counts + heatmap summary
- `GET /alerts/{id}`
- `POST /alerts/{id}/actions` – flag | freeze | report | escalate | dismiss

## Cases

- `GET /cases` – queue
- `POST /cases` – create
- `GET /cases/{id}`
- `POST /cases/{id}/notes`
- `PATCH /cases/{id}/assign`

## Reports

- `GET /reports/templates`
- `GET /reports/generate/{template_id}?format=pdf|csv`

All mutating actions write an immutable audit log entry.
