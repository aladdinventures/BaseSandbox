# CI/CD System Overview for Aladdin-sandbox Monorepo

## 1. Introduction

This document provides a high-level overview of the Continuous Integration/Continuous Deployment (CI/CD) system implemented for the `Aladdin-sandbox` monorepo. The system is designed to automate the build, test, and deployment processes for individual applications within the monorepo, ensuring efficiency, reliability, and maintainability.

## 2. Core Components

The CI/CD system leverages several key technologies and custom scripts:

*   **GitHub Actions**: The primary orchestration engine for all CI/CD workflows. It defines the sequence of jobs, steps, and conditions for each application.
*   **Render.com**: The cloud platform used for deploying applications. It supports various service types (web services, databases, cron jobs) and integrates with GitHub for automated deployments.
*   **MAMOS Runner (`mamos_runner.py`)**: A custom Python script responsible for executing project-specific test automation and triggering deployments to Render.com.
*   **Validation Script (`validate_project.py`)**: A custom Python script that performs initial checks, such as verifying project configuration in `projects.yaml` and ensuring necessary Render API Keys are set as GitHub Secrets.
*   **`config/projects.yaml`**: A centralized configuration file that defines each application within the monorepo, including its path, Render service IDs, and associated GitHub Secret names for API keys.

## 3. CI/CD Workflow Philosophy

The system adheres to the following principles:

*   **Project-Specific Workflows**: Each application within the monorepo has its own dedicated GitHub Actions workflow, triggered only when changes occur within its specific directory.
*   **Automated Testing**: Comprehensive test automation is integrated into the CI pipeline to ensure code quality and functionality before deployment.
*   **Environment-Based Deployments**: Deployments are structured across distinct environments: `Test`, `Staging`, and `Production`, each with its own set of configurations and protection rules.
*   **Manual Approval for Sensitive Deployments**: Deployments to `Staging` and `Production` environments require manual approval, providing a critical human gate for quality assurance and risk mitigation.
*   **Pre-Deployment Validation**: An initial validation step ensures that project configurations and required secrets are correctly set up, preventing common deployment failures.
*   **Security Best Practices**: Utilization of GitHub Secrets for sensitive information, minimal `permissions` for workflow jobs, and `concurrency` controls to prevent race conditions.

## 4. High-Level Workflow Execution Flow

1.  **Code Push/Pull Request**: A developer pushes code to a feature branch or opens a Pull Request targeting the `main` branch.
2.  **Workflow Trigger**: GitHub Actions detects changes in a specific application's directory and triggers its corresponding CI/CD workflow.
3.  **Validation Job**: The `validate` job runs first, using `validate_project.py` to check `projects.yaml` configuration and GitHub Secrets.
4.  **Build and Test Job**: If validation passes, the `build-and-test` job executes, performing project-specific builds and running MAMOS test automation.
5.  **Deploy to Test Environment**: Upon successful build and test, the application is automatically deployed to the `Test` environment via Render.com.
6.  **Deploy to Staging Environment (Manual Approval)**: Deployment to `Staging` requires manual approval in GitHub Actions. Once approved, the application is deployed to Render.com's Staging environment.
7.  **Deploy to Production Environment (Manual Approval)**: Deployment to `Production` requires a second manual approval. After successful verification in Staging and approval, the application is deployed to Render.com's Production environment.

This structured approach ensures that only thoroughly tested and approved code reaches production, maintaining the stability and integrity of the `Aladdin-sandbox` monorepo.

---
Copyright (c) 2025 Saeed Alaediny, Aladdin Trading LTD. All rights reserved.
