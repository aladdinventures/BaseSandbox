#!/usr/bin/env python3
"""
Copyright (c) 2025 Saeed Alaediny
This file is part of MAMOS (Manus Agent Management & Orchestration System)
"""

import os
import sys
import time
import platform
import psutil
import socket
import subprocess
import requests
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mamos-agent')


class MAMOSAgent:
    """MAMOS Agent - Lightweight client for agent management and orchestration"""
    
    def __init__(self, config_path: str = 'agent.yaml'):
        self.config = self.load_config(config_path)
        self.agent_id: Optional[str] = None
        self.server_url = self.config.get('server_url', 'http://localhost:4000')
        self.token = self.config.get('token')
        self.interval = self.config.get('interval', 30)
        self.hostname = socket.gethostname()
        
        if not self.token:
            logger.error('Registration token not found in config')
            sys.exit(1)
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f'Config file not found: {config_path}')
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f'Error parsing config file: {e}')
            sys.exit(1)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Collect system information"""
        return {
            'hostname': self.hostname,
            'os': f'{platform.system()} {platform.release()}',
            'cpuCores': psutil.cpu_count(),
            'ramTotal': int(psutil.virtual_memory().total / (1024 * 1024)),  # MB
            'ramUsed': int(psutil.virtual_memory().used / (1024 * 1024)),  # MB
        }
    
    def register(self) -> bool:
        """Register agent with orchestrator"""
        try:
            logger.info('Registering agent with orchestrator...')
            system_info = self.get_system_info()
            
            response = requests.post(
                f'{self.server_url}/agents/register',
                json=system_info,
                headers={'Authorization': f'Bearer {self.token}'},
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.agent_id = data.get('id')
                logger.info(f'Agent registered successfully: {self.agent_id}')
                return True
            else:
                logger.error(f'Registration failed: {response.status_code} - {response.text}')
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f'Registration error: {e}')
            return False
    
    def send_heartbeat(self) -> bool:
        """Send heartbeat to orchestrator"""
        if not self.agent_id:
            logger.error('Agent not registered, cannot send heartbeat')
            return False
        
        try:
            ram_used = int(psutil.virtual_memory().used / (1024 * 1024))
            
            response = requests.post(
                f'{self.server_url}/agents/{self.agent_id}/heartbeat',
                json={'ramUsed': ram_used},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.debug('Heartbeat sent successfully')
                return True
            else:
                logger.warning(f'Heartbeat failed: {response.status_code}')
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f'Heartbeat error: {e}')
            return False
    
    def fetch_pending_jobs(self):
        """Fetch pending jobs from orchestrator"""
        if not self.agent_id:
            return []
        
        try:
            response = requests.get(
                f'{self.server_url}/jobs/pending/{self.agent_id}',
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f'Failed to fetch jobs: {response.status_code}')
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching jobs: {e}')
            return []
    
    def execute_job(self, job: Dict[str, Any]) -> None:
        """Execute a job"""
        job_id = job.get('id')
        command = job.get('command')
        
        logger.info(f'Executing job {job_id}: {command}')
        
        # Update job status to running
        self.update_job_status(job_id, 'running')
        
        try:
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info(f'Job {job_id} completed successfully')
                self.update_job_status(job_id, 'completed', output=result.stdout)
            else:
                logger.error(f'Job {job_id} failed with return code {result.returncode}')
                self.update_job_status(job_id, 'failed', error=result.stderr)
                
        except subprocess.TimeoutExpired:
            logger.error(f'Job {job_id} timed out')
            self.update_job_status(job_id, 'failed', error='Command timed out')
        except Exception as e:
            logger.error(f'Job {job_id} execution error: {e}')
            self.update_job_status(job_id, 'failed', error=str(e))
    
    def update_job_status(self, job_id: str, status: str, output: str = None, error: str = None) -> None:
        """Update job status in orchestrator"""
        try:
            data = {'status': status}
            if output:
                data['output'] = output
            if error:
                data['error'] = error
            
            response = requests.put(
                f'{self.server_url}/jobs/{job_id}',
                json=data,
                timeout=10
            )
            
            if response.status_code != 200:
                logger.warning(f'Failed to update job status: {response.status_code}')
                
        except requests.exceptions.RequestException as e:
            logger.error(f'Error updating job status: {e}')
    
    def run(self) -> None:
        """Main agent loop"""
        logger.info('Starting MAMOS Agent...')
        
        # Register agent
        if not self.register():
            logger.error('Failed to register agent, exiting')
            sys.exit(1)
        
        logger.info(f'Agent running with {self.interval}s interval')
        
        try:
            while True:
                # Send heartbeat
                self.send_heartbeat()
                
                # Fetch and execute pending jobs
                jobs = self.fetch_pending_jobs()
                for job in jobs:
                    self.execute_job(job)
                
                # Wait for next iteration
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            logger.info('Agent stopped by user')
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            sys.exit(1)


if __name__ == '__main__':
    agent = MAMOSAgent()
    agent.run()

