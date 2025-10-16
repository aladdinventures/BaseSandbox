# Troubleshooting Guide for Aladdin-sandbox Monorepo CI/CD

## 1. Introduction

This guide provides solutions to common issues and errors encountered during the Continuous Integration/Continuous Deployment (CI/CD) process for the `Aladdin-sandbox` monorepo. When a CI/CD workflow fails, reviewing the logs is the first step. This guide will help you interpret those logs and identify potential fixes.

## 2. Common CI/CD Errors and Solutions

### 2.1. Workflow Not Triggering

**Problem**: A push or Pull Request was made, but no GitHub Actions workflow started.

**Possible Causes & Solutions**:
*   **Incorrect `paths` filter**: The `on.push.paths` or `on.pull_request.paths` in your workflow YAML might not match the changed files. Ensure the path pattern (`apps/your-project-name/**`) correctly covers the modified files.
*   **Incorrect `branches` filter**: The `on.push.branches` or `on.pull_request.branches` might not include the branch you pushed to (e.g., pushing to a feature branch not listed).
*   **Workflow file syntax error**: A syntax error in the `.github/workflows/*.yml` file can prevent it from being parsed by GitHub Actions. Check the YAML syntax.
*   **GitHub App Permissions**: The GitHub App (Manus Connector) might not have `Read` access to `Workflows`. Verify permissions in `Settings` -> `Developer settings` -> `GitHub Apps` -> `Manus Connector` -> `Permissions & events`.

### 2.2. `validate` Job Failure

**Problem**: The `validate` job fails with an error message from `validate_project.py`.

**Possible Causes & Solutions**:
*   **Project not found in `config/projects.yaml`**: The project name passed to `validate_project.py` (e.g., `python infra/ci-cd/validate_project.py backend`) does not exist as a top-level key in `config/projects.yaml`. Ensure the project name is correct and present.
*   **Missing `render_service_id`**: The `render_service_id` for a specific environment (Test, Staging, Production) is missing or malformed in `config/projects.yaml` for the project. Update `projects.yaml` with correct Render Service IDs.
*   **Missing Render API Key Secret**: The corresponding GitHub Secret for the Render API Key (e.g., `RENDER_BACKEND_TEST_API_KEY`) is not defined in GitHub. Add the secret in `Settings` -> `Secrets and variables` -> `Actions` (or environment secrets).
*   **Python/PyYAML installation issue**: The `validate_project.py` script requires Python and `pyyaml`. Check the `Install Python and dependencies` and `Install pyyaml` steps in the workflow logs.

### 2.3. `build-and-test` Job Failure

**Problem**: The `build-and-test` job fails.

**Possible Causes & Solutions**:
*   **Build errors**: The application failed to build. Review the logs for compiler errors, missing dependencies, or incorrect build commands.
*   **Test failures**: MAMOS test automation failed. Review the logs for specific test case failures reported by `mamos_runner.py`. This indicates a code issue that needs to be addressed.
*   **Missing dependencies**: Project-specific dependencies (e.g., `requirements.txt` for Python, `package.json` for Node.js) were not installed correctly. Check the `Install dependencies` step logs.
*   **`mamos_runner.py` issues**: The `mamos_runner.py` script itself might have an error or cannot find the project's test suite. Verify the script path and project structure.

### 2.4. `deploy-test` Job Failure

**Problem**: The automatic deployment to the `Test` environment fails.

**Possible Causes & Solutions**:
*   **Render API Key issue**: The `RENDER_<PROJECT_NAME>_TEST_API_KEY` secret is incorrect or expired. Verify the secret value in GitHub and generate a new API Key on Render.com if necessary.
*   **Render Service ID mismatch**: The `render_service_id` in `config/projects.yaml` for the Test environment does not match an existing service on Render.com. Verify the Service ID on Render.com.
*   **Render.com service configuration**: The Render service itself might be misconfigured (e.g., incorrect build command, start command, environment variables). Check Render.com service logs.
*   **Network issues**: Temporary connectivity issues between GitHub Actions and Render.com. Retrying the workflow might resolve this.

### 2.5. `deploy-staging` / `deploy-production` Job Stuck or Failure

**Problem**: Deployment to Staging or Production is stuck or fails after manual approval.

**Possible Causes & Solutions**:
*   **Awaiting Manual Approval**: The workflow is paused, waiting for a `Required reviewer` to approve the deployment. Check the GitHub Actions interface for the yellow circle icon and the prompt to review the deployment.
*   **Incorrect Environment Protection Rules**: The `Required reviewers` are not correctly configured for the environment in GitHub (`Settings` -> `Environments`). Ensure the correct users/teams are assigned.
*   **Render API Key/Service ID issues**: Similar to `deploy-test`, verify the Render API Key and Service ID for the specific Staging/Production environment.
*   **Post-deployment Health Checks**: If the deployment appears successful on Render but the application is not functioning, check Render.com service logs for runtime errors or issues with health checks defined on Render.

### 2.6. GitHub App Permissions Issue

**Problem**: Workflows fail with permission errors, especially related to `workflows` scope.

**Possible Causes & Solutions**:
*   **Insufficient Permissions**: The GitHub App (Manus Connector) does not have sufficient permissions to run workflows or access necessary resources. Ensure it has `Read and write` access for `Workflows` in `Settings` -> `Developer settings` -> `GitHub Apps` -> `Manus Connector` -> `Permissions & events`.

## 3. General Troubleshooting Tips

*   **Read Logs Carefully**: Always start by thoroughly reading the GitHub Actions workflow logs. Error messages often provide direct clues.
*   **Isolate the Problem**: Try to narrow down the issue to a specific job or step. If `validate` fails, focus there before looking at `build-and-test`.
*   **Reproduce Locally**: If possible, try to reproduce the issue locally (e.g., running `mamos_runner.py` or `validate_project.py` commands) to get more immediate feedback.
*   **Check Render.com Dashboard**: For deployment issues, the Render.com dashboard and service logs are invaluable.
*   **Consult Documentation**: Refer to this guide, the `SYSTEM_OVERVIEW.md`, `DEVELOPER_GUIDE.md`, and `DEPLOYMENT_GUIDE.md` for context and specific instructions.

---
Copyright (c) 2025 Saeed Alaediny, Aladdin Trading LTD. All rights reserved.
