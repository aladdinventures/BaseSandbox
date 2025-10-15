# MAMOS Agent

**Copyright (c) 2025 Saeed Alaediny**

Lightweight Python client agent for MAMOS (Manus Agent Management & Orchestration System).

## Features

- Agent registration with orchestrator
- Periodic heartbeat monitoring
- Job execution with whitelisted commands
- System information collection (OS, CPU, RAM)
- Configurable via YAML

## Requirements

- Python 3.11+
- pip

## Installation

### Quick Install

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy the example configuration:
   ```bash
   cp agent.yaml.example agent.yaml
   ```

2. Edit `agent.yaml` and set your configuration:
   ```yaml
   server_url: http://your-orchestrator-url:4000
   token: your_registration_token_here
   interval: 30
   ```

3. Get a registration token from the MAMOS Dashboard (Agents page → Create Registration Token)

## Usage

### Run Agent

```bash
python main.py
```

### Run as Background Service

#### Linux (systemd)

Create `/etc/systemd/system/mamos-agent.service`:

```ini
[Unit]
Description=MAMOS Agent
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/agent
ExecStart=/path/to/agent/venv/bin/python /path/to/agent/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mamos-agent
sudo systemctl start mamos-agent
sudo systemctl status mamos-agent
```

#### Windows (Task Scheduler)

Use the provided PowerShell installer script or manually create a scheduled task.

## Whitelisted Commands

For security, only the following commands are allowed:

- `echo`
- `ls`
- `pwd`
- `date`
- `whoami`
- `hostname`
- `uptime`
- `df`
- `free`

## Troubleshooting

### Agent fails to register

- Check that the orchestrator is running and accessible
- Verify the registration token is valid and not expired
- Check network connectivity

### Heartbeat failures

- Ensure the orchestrator is running
- Check network connectivity
- Verify the agent ID is valid

### Job execution failures

- Check that the command is in the whitelist
- Verify command syntax
- Check agent logs for detailed error messages

## License

MIT License - See LICENSE file for details

