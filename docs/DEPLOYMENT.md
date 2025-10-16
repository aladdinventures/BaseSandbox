# Copyright (c) 2025 Saeed Alaediny
# MAMOS Deployment Guide

This document outlines the deployment process for the MAMOS (Manus Agent Management & Orchestration System) platform.

## 1. Prerequisites

Before deploying MAMOS, ensure you have the following installed:

*   **Docker**: Containerization platform.
*   **Docker Compose**: Tool for defining and running multi-container Docker applications.

## 2. Deployment Steps

### 2.1. Clone the Repository

First, clone the `aladdin-sandbox` repository to your server:

```bash
git clone https://github.com/aladdinventures/aladdin-sandbox.git
cd aladdin-sandbox
```

### 2.2. Copy MAMOS Files

Copy the MAMOS specific files into their respective locations within the monorepo:

```bash
# Assuming you have the mamos-phase1 content in a temporary directory
# Copy backend (Orchestrator)
cp -r /path/to/mamos-phase1/apps/backend/mamos apps/backend/

# Copy frontend (Dashboard)
cp -r /path/to/mamos-phase1/apps/frontend/mamos apps/frontend/

# Copy agent
cp -r /path/to/mamos-phase1/apps/agent/mamos apps/agent/

# Copy infrastructure
cp -r /path/to/mamos-phase1/infra/docker/mamos infra/docker/
cp -r /path/to/mamos-phase1/infra/grafana/* infra/grafana/
cp -r /path/to/mamos-phase1/infra/prometheus/* infra/prometheus/

# Copy scripts and docs
cp /path/to/mamos-phase1/scripts/* scripts/
cp /path/to/mamos-phase1/docs/* docs/
```

### 2.3. Configure Environment Variables

Create a `.env` file for the Orchestrator in `infra/docker/mamos/.env`:

```env
NODE_ENV=production
PORT=4000
DATABASE_URL=file:./prod.db
JWT_SECRET=YOUR_VERY_STRONG_SECRET_KEY_HERE
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_secure_admin_password
```

### 2.4. Start Services

Navigate to the Docker Compose directory and start the services:

```bash
cd infra/docker/mamos
docker compose -f docker-compose.dev.yml up -d
```

This will bring up the Orchestrator, Dashboard, Prometheus, and Grafana services.

## 3. Accessing Services

*   **MAMOS Dashboard**: `http://localhost:3000`
*   **MAMOS Orchestrator API**: `http://localhost:4000`
*   **Grafana**: `http://localhost:3001` (Default login: `admin`/`admin`)
*   **Prometheus**: `http://localhost:9090`

## 4. Agent Deployment

Refer to the [Agent Setup Guide](AGENT.md) for instructions on deploying and configuring MAMOS Agents.

---

**Note:** This is a stub. More detailed deployment strategies (e.g., production-ready Docker Compose, Kubernetes, cloud deployments) will be added here as the project evolves.
