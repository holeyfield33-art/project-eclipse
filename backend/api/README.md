# Eclipse FastAPI Gateway

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs

## Environment

Copy from root `.env.example` (create one) or set:

- `DATABASE_URL`
- `NEO4J_URI` / `NEO4J_USER` / `NEO4J_PASSWORD`
- `ELASTICSEARCH_URL`
- `KAFKA_BOOTSTRAP`
- `REDIS_URL`
- `SECRET_KEY`

## Next implementation steps

1. Wire SQLAlchemy models + Alembic migrations
2. Implement JWT auth with role claims
3. Connect Neo4j driver for entity graph
4. Connect Elasticsearch for search
5. Call ML scoring service on new transactions
6. Immutable audit log middleware
