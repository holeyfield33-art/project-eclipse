# Eclipse Architecture

## High-Level Design

Eclipse follows a modular, cloud-native architecture optimized for real-time threat detection while preserving privacy (hashed identifiers only).

### Layers

1. **Ingestion** – Apache Kafka + Debezium connectors pull from SWIFT/FedWire/ACH, blockchain explorers, corporate registries, OFAC lists, dark-web scrapers, and internal logs.
2. **Storage**
   - PostgreSQL: relational data (users, cases, audit logs, transaction metadata)
   - Neo4j: entity graph (people, companies, wallets, relationships)
   - Elasticsearch: full-text search and alert/entity indexing
3. **ML Engine** – Risk scoring (logistic regression + SHAP), unsupervised anomaly detection, predictive forecasting. Served via FastAPI microservice; models versioned and retrained offline.
4. **API Gateway** – FastAPI (Python) handles auth, RBAC, orchestration; Go microservices handle high-throughput paths.
5. **Frontend** – React + TypeScript + Tailwind analyst dashboard.
6. **Orchestration** – Kubernetes + Helm; zero-trust networking (mTLS), HSM-backed keys.

## Data Flow (simplified)

```
Sources → Kafka topics → Ingestion consumers →
  ├─ Entity resolution (Neo4j)
  ├─ Feature extraction → ML scoring → Risk score + SHAP
  └─ Alert generation → Elasticsearch + Postgres

Analyst Dashboard ← FastAPI ← (Postgres / Neo4j / ES / Redis)
```

## Security & Privacy

- No full PII stored; only salted hashes of identifiers
- AES-256 at rest, TLS 1.3 in transit
- Immutable audit trail for every decision and action
- Role-based access: Analyst, Manager, Admin, Auditor
- GDPR/CCPA deletion & export endpoints

## Scalability

- Horizontal scaling of Kafka consumers and Go services
- Stateless API tier behind load balancer
- Neo4j causal clustering / Elasticsearch cluster for production
