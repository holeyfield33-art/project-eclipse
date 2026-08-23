# Terraform – Cloud Infrastructure

Scaffold for provisioning VPC / private cloud environments on AWS, Azure, or GCP.

Typical modules:

- VPC / networking
- EKS / AKS / GKE cluster
- Managed Postgres (RDS / Azure DB / Cloud SQL) or self-managed
- Neo4j Aura or self-managed StatefulSet
- Elasticsearch (Elastic Cloud or self-managed)
- Kafka (MSK / Confluent / self-managed)
- Object storage for reports & model artifacts
- IAM roles & secrets

Do not commit `.tfstate` or secrets. Use remote state (S3 + DynamoDB, Azure Storage, GCS) and a secrets backend.
