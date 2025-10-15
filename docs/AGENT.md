# Copyright (c) 2025 Saeed Alaediny
# MAMOS Agent Setup Guide

This document provides instructions for setting up and configuring the MAMOS Agent.

## 1. Agent Overview

The MAMOS Agent is a lightweight Python client responsible for:

*   Registering with the MAMOS Orchestrator.
*   Sending periodic heartbeats and system metrics.
*   Executing whitelisted commands dispatched by the Orchestrator.
*   Reporting job results back to the Orchestrator.

## 2. Prerequisites

*   **Python 3.11+**: Ensure Python is installed on the target machine.
*   **Orchestrator URL**: The URL of your running MAMOS Orchestrator.
*   **Registration Token**: A one-time token generated from the MAMOS Dashboard for agent registration.

## 3. Installation

### 3.1. Copy Agent Files

Copy the MAMOS Agent files to your target machine. For example, to `/opt/mamos-agent`:

```bash
sudo mkdir -p /opt/mamos-agent
sudo cp -r /path/to/aladdin-sandbox/apps/agent/mamos/* /opt/mamos-agent/
cd /opt/mamos-agent
```

### 3.2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3.3. Configure Agent

Copy the example configuration file and edit it:

```bash
cp agent.yaml.example agent.yaml
nano agent.yaml
```

Update the `server_url` and `registration_token` fields in `agent.yaml`.

## 4. Usage

### 4.1. Test Connection

Before running, test the agent's connection to the Orchestrator:

```bash
python mamos_agent.py test --config agent.yaml
```

### 4.2. Run Agent Manually

To run the agent in the foreground:

```bash
python mamos_agent.py run --config agent.yaml
```

### 4.3. Run as a Systemd Service (Linux)

For production environments, it's recommended to run the agent as a systemd service.

1.  Create a systemd service file (e.g., `/etc/systemd/system/mamos-agent.service`):

    ```ini
    [Unit]
    Description=MAMOS Agent
    After=network.target

    [Service]
    Type=simple
    User=your_user_here # e.g., ubuntu
    WorkingDirectory=/opt/mamos-agent
    ExecStart=/usr/bin/python3 /opt/mamos-agent/mamos_agent.py run --config /opt/mamos-agent/agent.yaml
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

2.  Reload systemd, enable, and start the service:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable mamos-agent
    sudo systemctl start mamos-agent
    sudo systemctl status mamos-agent
    ```

## 5. Configuration Options

*   `server_url`: The base URL of the MAMOS Orchestrator (e.g., `http://localhost:4000`).
*   `registration_token`: A unique, one-time token for agent registration.
*   `heartbeat_interval`: The interval (in seconds) at which the agent sends heartbeats to the Orchestrator (default: 30).
*   `metrics_port`: The port on which the agent exposes Prometheus metrics (default: 9101).
*   `allowed_commands`: A list of commands that the agent is permitted to execute. **This is a critical security feature.**

---

**Note:** This is a stub. More detailed troubleshooting, advanced configurations, and security best practices will be added here as the project evolves.
