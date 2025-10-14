# 🏗️ Infrastructure / زیرساخت

## Overview / نمای کلی

This directory contains Infrastructure as Code (IaC) configurations, CI/CD scripts, and DevOps tooling for the Aladdin Monorepo.

این پوشه شامل پیکربندی‌های زیرساخت به عنوان کد (IaC)، اسکریپت‌های CI/CD و ابزارهای DevOps برای Aladdin Monorepo است.

## Structure / ساختار

```
infra/
├── ci-cd/              # CI/CD scripts and automation
│   ├── mamos_runner.py # MAMOS test automation runner
│   └── deploy.sh       # Deployment scripts
├── docker/             # Docker configurations (future)
├── kubernetes/         # Kubernetes manifests (future)
└── terraform/          # Terraform IaC (future)
```

## CI/CD Directory / پوشه CI/CD

The `ci-cd/` directory contains automation scripts for continuous integration and deployment:

### mamos_runner.py

The MAMOS (Modular Autonomous Manager of Systems) runner is responsible for:

- Reading project configurations from `config/projects.yaml`
- Running automated tests on all projects
- Generating bilingual test reports (English/Persian)
- Monitoring application health
- Creating deployment summaries

**Usage:**

```bash
python infra/ci-cd/mamos_runner.py
```

**Output:**
- `reports/summary.md`: Overall test summary
- `reports/details/*.md`: Detailed reports per project

### deploy.sh

Deployment script for automated deployment to various environments.

**Usage:**

```bash
./infra/ci-cd/deploy.sh [environment]
# environment: test, staging, production
```

## GitHub Actions Integration / یکپارچگی با GitHub Actions

The infrastructure scripts are integrated with GitHub Actions workflows defined in `.github/workflows/`:

- **ci.yml**: Main CI/CD pipeline
- Triggers on push and pull requests
- Runs MAMOS tests automatically
- Uploads reports as artifacts

## Environment Management / مدیریت محیط‌ها

### GitHub Environments

Three environments are configured:

| Environment | Purpose | Protection Rules |
|-------------|---------|------------------|
| **test** | Automated testing | None |
| **staging** | Pre-production testing | Wait timer (5 min) |
| **production** | Live deployment | Required reviewers + Branch allowlist |

### Secrets Management / مدیریت Secrets

Sensitive configuration is managed via GitHub Secrets:

- `DATABASE_URL`: Database connection string
- `API_KEYS`: External service API keys
- `DEPLOY_TOKEN`: Deployment authentication token

**Never commit secrets to the repository!**

**هرگز secrets را در ریپوزیتوری commit نکنید!**

## Future Enhancements / بهبودهای آینده

- **Docker**: Containerization for consistent environments
- **Kubernetes**: Orchestration for scalable deployments
- **Terraform**: Infrastructure provisioning automation
- **Monitoring**: Integration with monitoring services (Datadog, New Relic)

---

**Maintained by**: DevOps Team  
**Last Updated**: 2025-10-14

