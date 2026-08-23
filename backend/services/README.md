# Eclipse Go Microservices

Placeholder for high-throughput Go services:

- **ingestion-service** – Kafka consumers for SWIFT/FedWire/ACH, blockchain, OFAC, dark-web feeds
- **scoring-service** – real-time risk score calculation (calls ML service or embeds model)
- **alert-service** – alert generation, prioritization, notification
- **graph-service** – Neo4j write path for entity resolution

## Suggested layout

```
services/
├── ingestion/
│   ├── main.go
│   ├── go.mod
│   └── ...
├── scoring/
├── alert/
└── graph/
```

Use `go mod init github.com/holeyfield33-art/project-eclipse/backend/services/<name>` for each service.

Target: low-latency, high-concurrency processing of transaction streams.
