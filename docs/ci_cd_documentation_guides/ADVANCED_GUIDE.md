# Advanced Guide for Aladdin-sandbox Monorepo CI/CD

## 1. Introduction

This advanced guide delves into the internal workings of the custom scripts and provides insights for power users, maintainers, and those looking to extend or deeply understand the `Aladdin-sandbox` monorepo CI/CD system. It covers `mamos_runner.py` and `validate_project.py`.

## 2. `mamos_runner.py` - The MAMOS CI/CD Orchestrator

`mamos_runner.py` is a Python script designed to act as the central execution point for project-specific CI/CD tasks within the monorepo. It abstracts away the complexities of running tests and triggering deployments.

### 2.1. Purpose and Functionality

*   **Project-Specific Execution**: It takes a `--project` argument to identify which application within the monorepo it should operate on.
*   **Test Automation**: When executed without a `--deploy-env` argument, it runs the MAMOS test automation suite for the specified project.
*   **Render Deployment Trigger**: When executed with a `--deploy-env` argument (e.g., `Test`, `Staging`, `Production`), it triggers a deployment to the corresponding Render.com service.
*   **Configuration Lookup**: It reads `config/projects.yaml` to retrieve project-specific configurations, including Render service IDs and GitHub Secret names for API keys.

### 2.2. Key Arguments

*   `--project <project_name>`: (Required) Specifies the name of the project (e.g., `backend`, `frontend`) to operate on. This name must match a top-level key in `config/projects.yaml`.
*   `--deploy-env <environment_name>`: (Optional) If provided, the script will attempt to trigger a deployment to the specified environment (e.g., `Test`, `Staging`, `Production`).

### 2.3. Internal Logic (Simplified)

1.  **Argument Parsing**: Uses `argparse` to process command-line arguments.
2.  **Configuration Loading**: Loads `config/projects.yaml` using `pyyaml`.
3.  **Project Validation**: Checks if the specified `--project` exists in `projects.yaml`.
4.  **Test Execution (if no `--deploy-env`)**: 
    *   Locates the project's test suite (e.g., `apps/<project_name>/tests/`).
    *   Executes the MAMOS test automation commands for that project.
    *   Reports test results.
5.  **Deployment Execution (if `--deploy-env` is present)**:
    *   Retrieves the `render_service_id` for the given project and environment from `projects.yaml`.
    *   Retrieves the Render API Key from environment variables (passed as GitHub Secrets).
    *   Constructs and sends an HTTP POST request to the Render Deploy Hook URL for the specified service, triggering a new deployment.
    *   Monitors the Render deployment status (optional, but can be extended).

### 2.4. Extending `mamos_runner.py`

*   **Adding New Deployment Targets**: Modify the deployment logic to support other deployment platforms (e.g., AWS, Azure) by adding new conditional branches based on environment variables or `projects.yaml` configurations.
*   **Enhanced Test Reporting**: Integrate with more sophisticated test reporting tools (e.g., JUnit XML) to provide richer test results in GitHub Actions.
*   **Post-Deployment Health Checks**: Add logic to perform automated health checks on the deployed application after Render reports a successful deployment.

## 3. `validate_project.py` - The Pre-Flight Checker

`validate_project.py` is a lightweight Python script designed to perform essential pre-flight checks before any build, test, or deployment process begins. Its primary goal is to catch common configuration errors early.

### 3.1. Purpose and Functionality

*   **Configuration Validation**: Ensures that a specified project exists in `config/projects.yaml`.
*   **Secret Validation**: Verifies that the necessary Render API Key GitHub Secrets are defined for each environment (Test, Staging, Production) for the given project.
*   **Early Failure**: If any validation check fails, the script exits with a non-zero status code, causing the GitHub Actions workflow to fail immediately, preventing further execution and saving resources.

### 3.2. Key Arguments

*   `<project_name>`: (Required, positional argument) The name of the project to validate.

### 3.3. Internal Logic (Simplified)

1.  **Argument Parsing**: Takes the project name as a command-line argument.
2.  **Configuration Loading**: Loads `config/projects.yaml`.
3.  **Project Existence Check**: Verifies if the `<project_name>` exists as a key in `projects.yaml`.
4.  **Render Secret Check**: For each environment (Test, Staging, Production) defined for the project in `projects.yaml`:
    *   It constructs the expected GitHub Secret name (e.g., `RENDER_BACKEND_TEST_API_KEY`).
    *   It checks if this environment variable is set (indicating the GitHub Secret is present).
    *   If any secret is missing, it prints an error and exits.

### 3.4. Extending `validate_project.py`

*   **Additional Configuration Checks**: Add checks for other critical configurations in `projects.yaml` (e.g., presence of a `build_command`, `test_command`).
*   **Environment Variable Checks**: Validate other required environment variables specific to a project.
*   **Schema Validation**: Implement a more robust schema validation for `projects.yaml` using libraries like `jsonschema` or `cerberus`.

## 4. GitHub Actions Workflow Structure

Each project's workflow (`.github/workflows/*.yml`) follows a consistent structure:

*   **`on` Trigger**: Configured with `push` and `pull_request` events, using `paths` filtering to trigger only for changes within the project's directory.
*   **`jobs`**: Defines a sequence of jobs:
    *   `validate`: Runs `validate_project.py`.
    *   `build-and-test`: Runs `mamos_runner.py` for testing.
    *   `deploy-test`: Runs `mamos_runner.py` for deployment to the `Test` environment.
    *   `deploy-staging`: Runs `mamos_runner.py` for deployment to `Staging`, with a manual approval step.
    *   `deploy-production`: Runs `mamos_runner.py` for deployment to `Production`, with a manual approval step.
*   **`needs`**: Ensures jobs run in the correct sequence (e.g., `deploy-test` needs `build-and-test`).
*   **`environment`**: Links deployment jobs to GitHub Environments, enabling protection rules and environment-specific secrets.
*   **`permissions`**: Explicitly sets minimal permissions for each job to enhance security.
*   **`concurrency`**: Prevents multiple concurrent runs of the same workflow for a given branch, avoiding race conditions.

Understanding this structure is key to debugging and extending the CI/CD system effectively.

---
Copyright (c) 2025 Saeed Alaediny, Aladdin Trading LTD. All rights reserved.
