# Deployment Guide

## Local Development

```bash
docker compose up -d          # Postgres, Neo4j, ES, Kafka, Redis
cd backend/api && uvicorn app.main:app --reload
cd frontend && npm run dev
```

## Kubernetes (Production)

See `infrastructure/k8s/` for starter manifests and Helm chart placeholders.

Minimum cluster: 3 nodes, 5–10 TB persistent storage (volume depends on transaction volume).

### Recommended order

1. Deploy stateful sets: Postgres, Neo4j, Elasticsearch, Kafka, Redis
2. Deploy ML scoring service
3. Deploy Go microservices (ingestion, scoring, alerts)
4. Deploy FastAPI gateway
5. Deploy frontend (static + CDN or Ingress)
6. Configure mTLS, secrets via HSM/Vault, network policies

## Cloud Options

- **SaaS multi-tenant** – managed by Eclipse operator
- **VPC / Private Cloud** – customer AWS / Azure / GCP account (Terraform in `infrastructure/terraform/`)
- **On-premise** – air-gapped; requires outbound allow-list for sanctioned data sources only

## Secrets

Never commit secrets. Use Kubernetes Secrets, external-secrets operator, or HashiCorp Vault. Hardware Security Modules (HSM) recommended for production key material.
