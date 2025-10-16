# Aladdin Sandbox

**A modern monorepo for managing multiple projects with shared infrastructure and tooling.**

---

## 📁 Repository Structure

This repository follows a standard monorepo structure optimized for scalability and maintainability:

```
aladdin-sandbox/
├── apps/                    # Complete applications
│   ├── mamos-dashboard/     # MAMOS Dashboard (Next.js/React)
│   ├── mamos-orchestrator/  # MAMOS Orchestrator (NestJS)
│   └── [other-apps]/        # Future applications
├── libs/                    # Shared libraries
│   ├── mamos/               # MAMOS shared utilities
│   └── shared/              # Common utilities
├── agents/                  # Agent applications
│   └── mamos/               # MAMOS Agent (Python)
├── infra/                   # Infrastructure configuration
│   ├── docker/              # Docker configurations
│   ├── prometheus/          # Prometheus configuration
│   └── grafana/             # Grafana dashboards
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
└── .github/                 # GitHub workflows and configurations
```

---

## 🚀 Current Projects

### MAMOS (Manus Agent Management & Orchestration System)

A complete platform for managing and orchestrating distributed agents.

**Components:**
- **Orchestrator** (`apps/mamos-orchestrator`): NestJS backend for agent management
- **Dashboard** (`apps/mamos-dashboard`): Next.js/React frontend
- **Agent** (`agents/mamos`): Python client agent
- **Monitoring**: Prometheus + Grafana integration

**Quick Start:**
```bash
# Start MAMOS services
cd infra/docker/mamos
docker-compose -f docker-compose.dev.yml up
```

**Access:**
- Dashboard: http://localhost:3000
- Orchestrator API: http://localhost:4000
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

---

## 📚 Documentation

- [MAMOS Architecture](docs/ARCHITECTURE.md)
- [MAMOS Deployment Guide](docs/DEPLOYMENT.md)
- [MAMOS Agent Setup](docs/AGENT.md)
- [Security Considerations](docs/SECURITY.md)

---

## 🛠️ Development

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- pnpm (for Node.js projects)

### Adding a New Project

When adding a new project to this monorepo:

1. **Applications**: Place in `apps/[project-name]/`
2. **Shared Libraries**: Place in `libs/[library-name]/`
3. **Agents**: Place in `agents/[agent-name]/`

### CI/CD

GitHub Actions workflows are configured in `.github/workflows/`:
- `ci.yml`: Continuous Integration for all projects

---

## 📝 License

Copyright (c) 2025 Saeed Alaediny. All rights reserved.

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

