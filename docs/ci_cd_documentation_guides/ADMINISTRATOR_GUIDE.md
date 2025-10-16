# Administrator Guide for Aladdin-sandbox Monorepo CI/CD

## 1. Introduction

This guide is intended for CI/CD administrators responsible for the setup, maintenance, and oversight of the `Aladdin-sandbox` monorepo's Continuous Integration/Continuous Deployment (CI/CD) system. It covers critical manual configurations and best practices for ensuring the system's security, reliability, and smooth operation.

## 2. Essential Manual Setup and Maintenance Tasks

### 2.1. Configuring GitHub Environments and Protection Rules

GitHub Environments are crucial for defining deployment targets and enforcing protection rules, especially for sensitive environments like Staging and Production.

1.  **Navigate to Repository Settings**: In your GitHub repository, go to `Settings`.
2.  **Access Environments**: In the left sidebar, click on `Environments`.
3.  **Create New Environments**: If not already present, create the following environments by clicking `New environment`:
    *   `Test`
    *   `Staging`
    *   `Production`
4.  **Configure Environment Protection Rules (for Staging and Production)**:
    *   For `Staging` and `Production` environments, click on the environment name, then `Configure environment`.
    *   **Required reviewers**: Enable `Required reviewers` and select the teams or individual users who must approve deployments to this environment. This is a critical step for implementing manual approval gates.
    *   **Wait timer (Optional)**: Consider adding a `Wait timer` to introduce a delay before deployment starts, allowing for additional checks or notifications.
    *   **Deployment branches (Optional)**: Restrict which branches can deploy to specific environments (e.g., only `main` can deploy to `Production`).

### 2.2. Managing GitHub Secrets for Render API Keys

GitHub Secrets are used to securely store sensitive information, such as Render API Keys, which are required for deployments. These secrets are not exposed in logs and are only accessible by authorized workflows.

1.  **Generate Render API Key**: Log in to your Render.com account and generate an API Key. Keep this key secure.
2.  **Navigate to Repository Secrets**: In your GitHub repository, go to `Settings` -> `Secrets and variables` -> `Actions`.
3.  **Add Repository Secrets**: Click `New repository secret`.
    *   For each project and each environment (Test, Staging, Production) that deploys to Render, you will need a corresponding API Key secret. The naming convention in our workflows is `RENDER_<PROJECT_NAME>_<ENVIRONMENT>_API_KEY`.
    *   **Example**: For the `backend` project deploying to `Test`, the secret name should be `RENDER_BACKEND_TEST_API_KEY`. The value will be your Render API Key.
    *   Repeat this for all projects and environments (e.g., `RENDER_FRONTEND_STAGING_API_KEY`, `RENDER_GPT_AGENT_PRODUCTION_API_KEY`, etc.).
    *   **Note**: For environments with `Required reviewers`, you might consider defining these secrets at the **Environment level** rather than repository level for finer-grained access control. To do this, go to `Settings` -> `Environments`, select the environment, and add secrets there.

### 2.3. Onboarding a New Project into the CI/CD System

To add a new application (project) to the monorepo and integrate it with the CI/CD system:

1.  **Create Project Directory**: Create a new directory for your application under `apps/` (e.g., `apps/new-service`).
2.  **Develop Application**: Implement your application code, including necessary dependencies and tests.
3.  **Update `config/projects.yaml`**: Add an entry for your new project in `config/projects.yaml`. This entry must include:
    *   `path`: The relative path to your project (e.g., `apps/new-service`).
    *   `render_service_id`: The Render.com service ID for each environment (Test, Staging, Production). You will need to create these services manually on Render.com first.
    *   `render_api_key_secret_name`: The name of the GitHub Secret that holds the Render API Key for each environment.
    *   **Example `projects.yaml` entry for a new project `new-service`:**
        ```yaml
        new-service:
          path: apps/new-service
          render_service_id:
            Test: svc-xxxxxxxxxxxxxxxxxxxx
            Staging: svc-yyyyyyyyyyyyyyyyyyyy
            Production: svc-zzzzzzzzzzzzzzzzzzzz
          render_api_key_secret_name:
            Test: RENDER_NEW_SERVICE_TEST_API_KEY
            Staging: RENDER_NEW_SERVICE_STAGING_API_KEY
            Production: RENDER_NEW_SERVICE_PRODUCTION_API_KEY
        ```
4.  **Create Render Services**: Manually create the corresponding services (Web Service, Background Worker, etc.) for your new project in Render.com for each environment (Test, Staging, Production). Note down their Service IDs.
5.  **Add GitHub Secrets**: Create the necessary GitHub Secrets (e.g., `RENDER_NEW_SERVICE_TEST_API_KEY`) as described in Section 2.2.
6.  **Create GitHub Actions Workflow**: Create a new workflow file (`.github/workflows/new-service.yml`) by copying and adapting an existing project workflow (e.g., `backend.yml`). Ensure you update:
    *   `name`: To reflect the new project (e.g., `New Service CI/CD`).
    *   `paths`: To trigger only for changes in `apps/new-service/**`.
    *   `jobs.validate.run`: To use `python infra/ci-cd/validate_project.py new-service`.
    *   `jobs.build-and-test.run`: To execute tests specific to `new-service`.
    *   `jobs.deploy-*.environment.url`: Update the URLs to match your new service.
    *   `jobs.deploy-*.env`: Ensure the `RENDER_..._API_KEY` variables match the secrets you created.
7.  **Test the New Workflow**: Create a feature branch, make a small change in `apps/new-service`, push, and create a Pull Request to verify the new CI/CD workflow functions correctly through all environments.

## 3. Troubleshooting and Monitoring

Administrators should regularly monitor GitHub Actions runs and Render.com deployment logs. Refer to the `TROUBLESHOOTING_GUIDE.md` for common issues and their resolutions.

---
Copyright (c) 2025 Saeed Alaediny, Aladdin Trading LTD. All rights reserved.
