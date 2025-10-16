# Development Guide for Aladdin-sandbox Monorepo CI/CD System

## Introduction
This document is a development guide for the Continuous Integration/Continuous Deployment (CI/CD) system implemented in the `aladdin-sandbox` monorepo. The purpose of this guide is to provide necessary information for developers and DevOps engineers to extend, modify, and adapt the CI/CD system to new project requirements.

## 1. CI/CD System Architecture

Our CI/CD system is built upon two main components:

*   **`mamos_runner.py`**: A Python script that forms the core CI/CD logic. This script is responsible for reading project configurations, executing build and test commands, and interacting with deployment APIs (e.g., Render.com).
*   **GitHub Actions Workflows**: YAML files that define how `mamos_runner.py` is executed within the GitHub Actions environment. These Workflows manage triggers, environments, secrets, and the CI/CD execution steps.

## 2. Key Files for Development

*   **`infra/ci-cd/mamos_runner.py`**: 
    *   **Purpose**: Executes build, test, and deployment steps for a specific project.
    *   **Common Changes**: Adding support for new project types, improving reporting logic, adding new CI/CD stages (e.g., security scanning), or changing how it interacts with deployment platforms.
*   **`config/projects.yaml`**: 
    *   **Purpose**: Defines projects, their paths, build and test commands, and deployment configurations for each environment.
    *   **Common Changes**: Adding new projects, updating build/test commands for existing projects, changing deployment service IDs.
*   **`.github/workflows/<project_name>.yml`**: 
    *   **Purpose**: Defines the CI/CD Workflow for a specific project in GitHub Actions.
    *   **Common Changes**: Modifying Workflow triggers, adding new steps (e.g., additional manual approvals), updating environment variables, or changing Job permissions.

## 3. Adding a New Project to the Monorepo

To add a new project (e.g., `new_app`) to the monorepo and integrate it into the CI/CD system, follow these steps:

1.  **Create Project Folder**: Create the new project folder at `aladdin-sandbox/apps/new_app`.
2.  **Add Code and Dependencies**: Place the project code and dependency files (e.g., `requirements.txt` for Python or `package.json` for Node.js) within this folder.
3.  **Update `config/projects.yaml`**: Add a new entry for `new_app` in `config/projects.yaml`:
    ```yaml
      - name: new_app
        path: apps/new_app
        build: "<build command for new project>"
        test: "<test command for new project>"
        deploy:
          - environment: Test
            render_service_id: "new-app-test-service-id"
          - environment: Staging
            render_service_id: "new-app-staging-service-id"
          - environment: Production
            render_service_id: "new-app-production-service-id"
    ```
    *   `build`: The shell command to build the project (e.g., `pip install -r requirements.txt && python setup.py build`).
    *   `test`: The shell command to run the project's tests (e.g., `pytest` or `npm test`).
    *   `render_service_id`: Render.com service IDs for each environment. These IDs must be pre-created in Render.com.
4.  **Create GitHub Actions Workflow**: Create a new Workflow file in `aladdin-sandbox/.github/workflows/new_app.yml`. You can use existing Workflows as templates. Ensure that:
    *   Change the Workflow `name` to `New App CI/CD`.
    *   Set `on: push: paths:` to `apps/new_app/**` so the Workflow is only triggered by changes in this project.
    *   Set the `--project` parameter in the `mamos_runner.py` call to `new_app`.
    *   Properly configure deployment environments (`Test`, `Staging`, `Production`) and manual approvals.
5.  **Test**: `push` your changes to a new branch and manually run the new Workflow to ensure it functions correctly.

## 4. Modifying Existing Workflows

To modify an existing Workflow (e.g., `backend.yml`):

1.  **Edit the Workflow File**: Open the `aladdin-sandbox/.github/workflows/backend.yml` file.
2.  **Apply Desired Changes**: 
    *   **Add a New Step**: You can add a new `step` to existing Jobs (e.g., to run a security scan or a code quality analysis).
    *   **Change Triggers**: If you want the Workflow to be triggered under different conditions, modify the `on:` section.
    *   **Update Environment Variables**: Add new or modify existing environment variables.
    *   **Change Permissions**: If you add a new Job that requires more permissions, update the `permissions` block.
3.  **Test**: `push` the changes to a new branch and manually run the Workflow to ensure its correct operation.

## 5. Developing `mamos_runner.py`

If you need to change the core CI/CD logic, you will need to edit `mamos_runner.py`:

1.  **Understand `mamos_runner.py` Structure**: This script uses `argparse` to receive arguments (e.g., `--project`, `--deploy-env`). The main logic resides in functions like `run_build`, `run_test`, `run_deploy`, and `main`.
2.  **Apply Changes**: 
    *   **Add New Project Type Support**: If you want to support a new project type (e.g., Go or Java), you might need to add new logic within the `run_build` and `run_test` functions to execute commands specific to that language.
    *   **Improve Reporting**: You can change the report format or include more information in them.
    *   **Integrate with New Tools**: If the CI/CD system needs to integrate with a new tool (e.g., a static code analysis tool or another deployment platform), you must add the relevant API call logic or shell commands to `mamos_runner.py`.
3.  **Test**: After making changes, test `mamos_runner.py` locally with different parameters. Then, `push` the changes to a new branch and run the GitHub Actions Workflows to ensure no regressions are introduced.

## 6. Managing Secrets and Environment Variables

*   **Add New Secrets**: If a new project requires a new Secret (e.g., `NEW_API_KEY`), add it as a Secret in your GitHub repository settings (`Settings > Secrets and variables > Actions > New repository secret`).
*   **Use Secrets in Workflow**: In the relevant Workflow file, inject the new Secret as an environment variable into the desired Job or Step:
    ```yaml
    env:
      NEW_API_KEY: ${{ secrets.NEW_API_KEY }}
    ```
*   **Environment-Specific Variables**: For variables that are only valid in a specific environment (e.g., `Staging` or `Production`), you can define them in the GitHub Actions environment settings (`Settings > Environments > <Environment Name> > Environment secrets`).

## 7. Best Practices for Development

*   **Small, Frequent Changes**: Make changes in small increments and `commit` and `push` frequently.
*   **Test Before Merge**: Always test your changes in a separate branch and ensure they work correctly before merging into `main`.
*   **Code Review**: Changes to `mamos_runner.py` and GitHub Actions Workflows should be reviewed by peers.
*   **Documentation**: Document any significant changes to the CI/CD system in the relevant guides.
*   **Use `workflow_dispatch`**: For testing changes in Workflows, use `workflow_dispatch` for manual execution to prevent unintended Workflow triggers.

## 8. Support

In case of complex issues or a need for specialized assistance, consult the support team or CI/CD experts.
