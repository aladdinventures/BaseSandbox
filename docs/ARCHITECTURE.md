# Copyright (c) 2025 Saeed Alaediny
# MAMOS Architecture Overview

This document provides an overview of the MAMOS (Manus Agent Management & Orchestration System) architecture.

## 1. System Layers

MAMOS is composed of three main layers:

*   **Orchestrator Layer**: The central brain, responsible for agent management, job orchestration, and API services.
*   **Agent Layer**: Lightweight clients deployed on target machines, executing tasks and reporting status.
*   **Monitoring & Visualization Layer**: Collects metrics and provides dashboards for system health and performance.

## 2. Component Diagram

```mermaid
graph TD
    subgraph "Monitoring & Visualization Layer"
        Grafana[Grafana]
        Prometheus[Prometheus]
    end

    subgraph "Orchestrator Layer"
        Orchestrator(NestJS Orchestrator)
        Database(Prisma/SQLite)
    end

    subgraph "Agent Layer"
        Agent1(Python Agent 1)
        Agent2(Python Agent 2)
        AgentN(Python Agent N)
    end

    Agent1 -- Heartbeat & Job Results --> Orchestrator
    Agent2 -- Heartbeat & Job Results --> Orchestrator
    AgentN -- Heartbeat & Job Results --> Orchestrator

    Orchestrator -- Metrics Exposure --> Prometheus
    Agent1 -- Metrics Exposure --> Prometheus
    Agent2 -- Metrics Exposure --> Prometheus
    AgentN -- Metrics Exposure --> Prometheus

    Prometheus -- Data Source --> Grafana
    Dashboard(Next.js Dashboard) -- API Calls --> Orchestrator
    Dashboard -- Embed Grafana --> Grafana

    User[User] -- Access --> Dashboard
    User -- Interact --> Orchestrator
```

## 3. Data Flow

*   **Agent Registration**: Agents register with the Orchestrator using one-time tokens.
*   **Heartbeats**: Agents send periodic heartbeats and system metrics to the Orchestrator.
*   **Job Execution**: Orchestrator dispatches jobs to agents. Agents execute commands and report results.
*   **Metrics Collection**: Prometheus scrapes metrics from the Orchestrator and Agents.
*   **Visualization**: Grafana queries Prometheus to display real-time dashboards.

## 4. Technologies Used

| Component       | Technology Stack         | Description                                    |
| :-------------- | :----------------------- | :--------------------------------------------- |
| Orchestrator    | NestJS, TypeScript, Prisma | Backend API, Agent Management, Job Queue       |
| Agent           | Python, Typer, Requests  | Lightweight client, command execution, metrics |
| Dashboard       | Next.js, React, TailwindCSS| Web UI for monitoring and control              |
| Database        | SQLite (for MVP)         | Persistent storage for Orchestrator            |
| Monitoring      | Prometheus, Grafana      | Metrics collection and visualization           |
| Containerization| Docker, Docker Compose   | Development and deployment                     |

---

**Note:** This is a stub. More detailed architectural decisions, component interactions, and design patterns will be added here as the project evolves.
