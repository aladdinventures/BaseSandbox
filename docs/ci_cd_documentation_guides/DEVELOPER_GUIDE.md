# Developer Guide for Aladdin-sandbox Monorepo CI/CD

## 1. Introduction

This guide outlines the standard development workflow for contributing to the `Aladdin-sandbox` monorepo, focusing on how to interact with the Continuous Integration/Continuous Deployment (CI/CD) system. Following these steps ensures your changes are properly tested, reviewed, and deployed.

## 2. Standard Development Workflow

### 2.1. Start with a Feature Branch

Always develop new features, bug fixes, or improvements on a dedicated feature branch. This isolates your changes and prevents conflicts with the main codebase.

1.  **Update your local `main` branch**: Ensure your local `main` branch is up-to-date with the remote repository.
    ```bash
    git checkout main
    git pull origin main
    ```
2.  **Create a new feature branch**: Create a new branch from `main` with a descriptive name (e.g., `feature/add-new-api`, `bugfix/fix-login-issue`).
    ```bash
    git checkout -b feature/your-feature-name
    ```

### 2.2. Make Your Changes

Implement your code changes within the relevant application directory (e.g., `apps/backend`, `apps/frontend`). Ensure you write unit and integration tests for your new or modified code.

### 2.3. Run Local Tests

Before committing, run local tests to catch issues early. The `mamos_runner.py` script can be used for this:

```bash
python infra/ci-cd/mamos_runner.py --project your-project-name
```
Replace `your-project-name` with the actual name of the application you are working on (e.g., `backend`, `frontend`).

### 2.4. Commit Your Changes

Commit your changes frequently with clear and concise commit messages.

```bash
git add .
git commit -m "feat: Add new user authentication endpoint"
```

### 2.5. Push Your Feature Branch

Push your feature branch to the remote GitHub repository.

```bash
git push origin feature/your-feature-name
```

### 2.6. Create a Pull Request (PR)

Once your changes are complete and locally tested, create a Pull Request to merge your feature branch into the `main` branch.

1.  Go to your GitHub repository in your web browser.
2.  GitHub will usually prompt you to create a Pull Request from your newly pushed branch.
3.  Ensure the base branch is `main` and the compare branch is your feature branch.
4.  Provide a clear title and detailed description for your PR, explaining the changes, their purpose, and any relevant context.
5.  Request reviews from appropriate team members.

## 3. Monitoring CI/CD Workflow

After creating a Pull Request, GitHub Actions will automatically trigger the CI/CD workflow for your project.

1.  Navigate to the `Actions` tab in your GitHub repository.
2.  Find the workflow run associated with your Pull Request.
3.  **`validate` Job**: This job will run first, ensuring your project is correctly configured in `projects.yaml` and that necessary secrets are defined. If this fails, check `config/projects.yaml` and ensure GitHub Secrets are set up.
4.  **`build-and-test` Job**: This job will build your application and run all automated tests (MAMOS). If it fails, review the logs for test failures or build errors.
5.  **`deploy-test` Job**: If `build-and-test` passes, your application will be automatically deployed to the `Test` environment on Render.com. You can check the Render dashboard for deployment status.
6.  **`deploy-staging` Job (Manual Approval)**: Deployment to `Staging` requires manual approval. The workflow will pause, and you (or an assigned reviewer) will need to approve it in the GitHub Actions interface. **Always review the changes and prerequisites before approving.**
7.  **`deploy-production` Job (Manual Approval)**: Similar to Staging, deployment to `Production` requires another manual approval. This is the final gate before your changes go live. **Thoroughly verify the Staging deployment before approving Production.**

## 4. Interpreting CI/CD Results

*   **Green Checkmark (✅)**: Indicates a successful job or step. Your changes passed.
*   **Red Cross (❌)**: Indicates a failed job or step. Review the logs for details on what went wrong.
*   **Yellow Circle (🟡)**: Indicates a pending or in-progress job. For `deploy-staging` and `deploy-production`, this will appear when manual approval is required.

Always review the logs of failed jobs to understand the root cause. The `validate_project.py` script and `mamos_runner.py` provide helpful output in the logs.

---
Copyright (c) 2025 Saeed Alaediny, Aladdin Trading LTD. All rights reserved.
