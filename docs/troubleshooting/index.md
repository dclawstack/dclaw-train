# Troubleshooting

Common issues and solutions for DClaw Train.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-train

# Check logs
kubectl logs -n dclaw-train deployment/dclaw-train-backend

# Check database
kubectl get clusters -n dclaw-train
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
