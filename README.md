# Project Eclipse

**See threats before they surface.**

Eclipse is a modular, AI-powered threat intelligence and fraud detection platform designed for mid-sized banks, fintechs, insurance firms, and government agencies (non-classified).

It ingests data from multiple sources (transactions, public records, dark web feeds, and internal logs), applies machine learning to identify suspicious patterns, and delivers actionable alerts to security teams — all without storing or exposing sensitive customer data.

**Version:** 2.0 (Clean)  
**Status:** Ready for Development  
**License:** Apache 2.0

---

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Multi-source Ingestion** | Connects to SWIFT, FedWire, ACH, blockchain explorers, corporate registries, and dark web scrapers. |
| **Entity Resolution** | Builds a unified graph of people, companies, wallets, and transactions. |
| **Risk Scoring** | Assigns a dynamic 0–100 risk score to every entity based on behavior, linkages, and historical patterns. |
| **Anomaly Detection** | Uses unsupervised learning to flag deviations from normal transaction behavior. |
| **Predictive Alerts** | Forecasts likely next moves of tracked actors and suggests pre-emptive actions. |
| **Case Management** | Provides a workflow for analysts to investigate, annotate, and escalate alerts. |
| **Audit Trail** | Logs every decision and action for compliance (SEC, FINRA, GDPR, CCPA). |

---

## System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│  API Gateway     │────▶│  Microservices  │
│ React + TS +    │     │  FastAPI + Go    │     │  (Go services)  │
│ Tailwind        │     └──────────────────┘     └─────────────────┘
└─────────────────┘              │                        │
                                 ▼                        ▼
                    ┌──────────────────────┐   ┌─────────────────────┐
                    │   Data Ingestion     │   │   ML Engine         │
                    │ Kafka + Debezium     │   │ TF / PyTorch / SKL  │
                    └──────────────────────┘   └─────────────────────┘
                                 │                        │
                                 ▼                        ▼
                    ┌──────────────────────────────────────────────┐
                    │  Storage: PostgreSQL + Neo4j + Elasticsearch │
                    └──────────────────────────────────────────────┘
```

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React + TypeScript + Tailwind | Analyst dashboard |
| Backend | Python (FastAPI) + Go (microservices) | API gateway, orchestration, ML serving |
| Data Ingestion | Apache Kafka + Debezium | Real-time streaming from multiple sources |
| Storage | PostgreSQL + Neo4j + Elasticsearch | Structured data, entity relationships, search |
| ML Engine | TensorFlow + PyTorch + Scikit-learn | Anomaly detection, scoring, forecasting |
| Orchestration | Kubernetes + Helm | Scalable, cloud-native deployment |
| Security | Zero-trust, mTLS, HSM | End-to-end encryption and access control |

---

## Repository Structure

```
project-eclipse/
├── backend/
│   ├── api/                 # FastAPI gateway & core APIs
│   ├── services/            # Go microservices (ingestion, scoring, alerts)
│   └── ml/                  # ML models, training, serving
├── frontend/                # React + TypeScript + Tailwind dashboard
├── infrastructure/
│   ├── k8s/                 # Kubernetes manifests & Helm charts
│   └── terraform/           # Cloud infrastructure as code
├── data/
│   └── schemas/             # Avro/Protobuf schemas, DB migrations
├── docs/                    # Architecture, API, deployment guides
├── scripts/                 # Dev utilities, seed data, local setup
├── docker-compose.yml       # Local development stack
├── .gitignore
└── LICENSE
```

---

## Quick Start (Local Development)

### Prerequisites

- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- Go 1.22+
- kubectl (optional, for k8s)

### 1. Clone & Start Infrastructure

```bash
git clone https://github.com/holeyfield33-art/project-eclipse.git
cd project-eclipse

# Start Postgres, Neo4j, Elasticsearch, Kafka, Redis
docker compose up -d
```

### 2. Backend (FastAPI)

```bash
cd backend/api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard: http://localhost:5173

### 4. ML Service (optional)

```bash
cd backend/ml
pip install -r requirements.txt
python serve.py
```

---

## Data Sources (Ingestion Layer)

| Source | Type | Update Frequency |
|--------|------|------------------|
| SWIFT / FedWire / ACH | Financial transactions | Real-time |
| Blockchain explorers (BTC, ETH, XMR) | Crypto wallets & flows | 5-minute intervals |
| State corporate registries | LLC / corporation filings | Daily |
| OFAC / sanctions lists | Blacklisted entities | Hourly |
| Dark web scrapers (targeted) | Threat chatter | 15-minute intervals |
| Internal logs | Behavioral data | Real-time |

---

## Risk Scoring Algorithm (Explainable)

Each entity receives a **Risk Score (0–100)** based on weighted factors:

| Factor | Weight | Examples |
|--------|--------|----------|
| Transaction velocity | 25% | Sudden spike in volume or frequency |
| Linkages to high-risk entities | 20% | Connected to known shell companies or sanctioned individuals |
| Geographic red flags | 15% | Transfers to/from high-risk jurisdictions |
| Account age & activity | 10% | New accounts with unusually large transfers |
| Behavioral anomaly | 20% | Deviation from typical transaction patterns |
| Dark web mentions | 10% | Account or entity appears in threat chatter |

Factors are combined via logistic regression. **SHAP values** are provided for every score for full explainability.

---

## User Roles & Access Control

| Role | Permissions |
|------|-------------|
| **Analyst** | View alerts, investigate entities, annotate cases, generate reports |
| **Manager** | Approve/override alerts, assign cases, view team performance |
| **Admin** | Manage users, configure data sources, set scoring thresholds |
| **Auditor** | Read-only access to audit logs and compliance reports |

Zero-trust architecture with least-privilege RBAC, mutual TLS, and hardware-backed keys (HSM support).

---

## Dashboard Features

### Main View
- Threat Overview (High/Medium/Low risk counts, geographic heatmap)
- Live Feed of recent alerts with risk scores
- Entity Search (name, account, wallet, company)
- Case Queue with priority flags

### Entity Profile
- Summary, risk score, linked entities
- Transaction history timeline
- Interactive network graph (Neo4j-powered)
- Alerts history & actions (flag, freeze, report, escalate)

### Reports
- Pre-built SAR templates, compliance summaries, executive dashboards
- Custom PDF/CSV exports

---

## Compliance & Privacy

- **Data minimisation**: Never stores full PII — only hashed identifiers
- **Audit logging**: Immutable logs of every decision and action
- **RBAC**: Least-privilege model
- **GDPR / CCPA ready**: Built-in data deletion and export
- **Encryption**: AES-256 at rest, TLS 1.3 in transit

---

## Deployment Options

| Option | Description |
|--------|-------------|
| **SaaS (Multi-tenant)** | Fully managed, pay-per-use |
| **VPC / Private Cloud** | Deployed in customer cloud (AWS, Azure, GCP) |
| **On-premise** | Air-gapped or highly regulated environments |

**Minimum infrastructure:**
- Kubernetes cluster (3+ nodes)
- Persistent storage (5–10 TB depending on volume)
- Outbound access to data sources, inbound HTTPS for dashboard

See `docs/deployment.md` and `infrastructure/` for details.

---

## Pricing Model (Suggested)

| Tier | Monthly Price | Features |
|------|---------------|----------|
| **Starter** | $5,000 | Up to 1M tx/month, 1 data source, 5 users |
| **Professional** | $15,000 | Up to 10M tx/month, 5 data sources, 20 users, full ML |
| **Enterprise** | Custom | Unlimited, all sources, custom models, on-prem, dedicated support |

---

## Roadmap (Phase 1 – 3 Months)

| Week | Milestone |
|------|-----------|
| 1–2 | Core ingestion pipeline (Kafka + PostgreSQL + Neo4j) |
| 3–4 | Risk scoring algorithm (MVP) |
| 5–6 | Dashboard (React + FastAPI) |
| 7–8 | Integration with 3 data sources (test) |
| 9–10 | Anomaly detection module |
| 11–12 | Beta launch with 3 pilot clients |

---

## Team Requirements (for Build)

| Role | Count | Skills |
|------|-------|--------|
| Backend Engineer | 2 | Python, Go, Kafka, PostgreSQL |
| Data Engineer | 1 | ETL pipelines, data modeling, Neo4j |
| ML Engineer | 1 | TensorFlow, PyTorch, anomaly detection |
| Frontend Engineer | 1 | React, TypeScript, Tailwind |
| DevOps Engineer | 1 | Kubernetes, Helm, Terraform |
| Product Manager | 1 | Financial crime domain expertise |

---

## Success Metrics (for Clients)

- Reduction in false positives: **≥ 40%** (vs legacy rule-based systems)
- Detection lead time: **≤ 2 hours** (high-risk transactions)
- Investigation time: **≤ 20 minutes** per alert
- Compliance readiness: **100%** audit-ready logs

---

## Competitive Advantage

| Feature | Eclipse | Competitors (e.g. Palantir, SAS) |
|---------|---------|----------------------------------|
| Price | Affordable, modular | Expensive, rigid |
| Deployment | SaaS, private cloud, or on-premise | Mostly on-premise only |
| Explainability | SHAP values for all decisions | Black-box for many |
| Time-to-value | 4–6 weeks | 6–12 months |

---

## Development Status

This repository contains the **full specification scaffold** ready for implementation:

- FastAPI skeleton with auth, entities, alerts, cases endpoints
- Go microservice stubs for ingestion and scoring
- React + TypeScript dashboard skeleton with routing and layout
- Docker Compose for local Postgres / Neo4j / Elasticsearch / Kafka
- Kubernetes + Helm chart placeholders
- Risk scoring model interface + SHAP explainability stubs
- Comprehensive docs

See individual `README.md` files in each package for next implementation steps.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please follow the coding standards defined in each package and ensure tests pass.

---

## License

Copyright © 2026 Aletheia Sovereign Systems / Project Eclipse contributors.

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

---

## Contact & Next Steps

1. Build MVP using this scaffold
2. Pilot with 3 clients (banks or fintechs)
3. Iterate based on feedback
4. Go-to-market — direct sales + channel partners

**Tagline:** *See threats before they surface.*
