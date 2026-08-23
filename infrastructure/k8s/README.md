# Kubernetes Manifests & Helm

Placeholder directory for production deployment.

Recommended structure:

```
k8s/
├── base/           # Kustomize base
│   ├── namespace.yaml
│   ├── api-deployment.yaml
│   ├── ml-deployment.yaml
│   └── ...
├── overlays/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── charts/
    └── eclipse/    # Helm chart
```

Key concerns:

- Network policies (zero-trust)
- mTLS between services (Istio / Linkerd or cert-manager)
- Secrets via external-secrets + Vault / HSM
- PersistentVolumeClaims sized for expected transaction volume
- HorizontalPodAutoscaler on API and ingestion workers
