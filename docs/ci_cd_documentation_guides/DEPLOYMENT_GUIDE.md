# Deployment Guide for Aladdin-sandbox Monorepo (Render.com Integration)

## 1. Introduction

This guide provides detailed information on how the `Aladdin-sandbox` monorepo CI/CD system integrates with Render.com for application deployments. It covers understanding Render services, monitoring deployments, and troubleshooting Render-specific issues.

## 2. Understanding Render.com Integration

Our CI/CD system uses Render.com as the primary deployment platform. Each application within the monorepo, for each environment (Test, Staging, Production), corresponds to a specific service on Render.com.

### 2.1. Render Services

*   **Service Types**: Render supports various service types, including Web Services (for web applications and APIs), Background Workers (for long-running tasks), Cron Jobs (for scheduled tasks), and Databases.
*   **Service ID**: Each service on Render has a unique identifier (e.g., `svc-xxxxxxxxxxxxxxxxxxxx`). These IDs are crucial for our `config/projects.yaml` file, which maps our monorepo projects to their respective Render services.
*   **Automatic Builds and Deployments**: When a CI/CD workflow triggers a deployment, `mamos_runner.py` interacts with the Render API to initiate a new build and deployment for the specified service.

### 2.2. `config/projects.yaml` and Render Configuration

The `config/projects.yaml` file is the central place where Render service IDs and associated GitHub Secret names are defined for each project and environment. This allows `mamos_runner.py` to dynamically determine which Render service to deploy to and which API Key to use.

**Example `projects.yaml` entry:**

```yaml
backend:
  path: apps/backend
  render_service_id:
    Test: svc-1234567890abcdefg
    Staging: svc-abcdefg1234567890
    Production: svc-gfedcba0987654321
  render_api_key_secret_name:
    Test: RENDER_BACKEND_TEST_API_KEY
    Staging: RENDER_BACKEND_STAGING_API_KEY
    Production: RENDER_BACKEND_PRODUCTION_API_KEY
```

### 2.3. Render API Keys (GitHub Secrets)

Deployment to Render.com is authenticated using Render API Keys. These keys are stored securely as GitHub Secrets and are passed to the `mamos_runner.py` script during the deployment phase. Each environment typically uses a separate API Key for enhanced security.

## 3. Monitoring Deployments on Render.com

After a deployment job is triggered in GitHub Actions, you can monitor its status directly on Render.com.

1.  **Log in to Render.com Dashboard**: Access your Render.com account.
2.  **Navigate to Your Service**: Find the specific service corresponding to the project and environment being deployed (e.g., `backend-staging`).
3.  **View Deployment Logs**: On the service dashboard, you will see a list of recent deployments. Click on the active deployment to view real-time build and deployment logs. This is crucial for debugging any deployment failures.
4.  **Deployment Status**: Render provides clear status indicators (e.g., `Live`, `Building`, `Failed`).

## 4. Troubleshooting Render-Specific Deployment Issues

If a deployment to Render.com fails, follow these steps:

1.  **Check GitHub Actions Logs**: Review the logs of the `deploy-test`, `deploy-staging`, or `deploy-production` job in GitHub Actions. Look for any errors reported by `mamos_runner.py` or the Render API.
2.  **Check Render.com Deployment Logs**: Go to the Render.com dashboard for the specific service and examine its deployment logs. These logs often provide more detailed information about build failures, runtime errors, or configuration issues on the Render platform.
3.  **Verify `config/projects.yaml`**: Ensure that the `render_service_id` for the failing project and environment is correct and matches the actual Service ID on Render.com.
4.  **Verify GitHub Secrets**: Confirm that the `RENDER_<PROJECT_NAME>_<ENVIRONMENT>_API_KEY` secret is correctly defined in GitHub (either at the repository or environment level) and that its value is a valid Render API Key.
5.  **Render Service Configuration**: Check the configuration of your service on Render.com. Ensure that build commands, start commands, environment variables, and other settings are correct for your application.
6.  **Resource Limits**: For free tier services, be aware of resource limits. Deployment failures might occur due to insufficient memory or CPU during the build process.

## 5. Render Preview Environments (Advanced)

Render supports Preview Environments, which can be automatically created for each Pull Request. While our current setup focuses on Test, Staging, and Production, integrating Preview Environments can further enhance the development workflow by providing isolated environments for each feature branch. This would require additional configuration in Render and potentially modifications to the GitHub Actions workflows to dynamically create and tear down these environments.

---
Copyright (c) 2025 Saeed Alaediny, Aladdin Trading LTD. All rights reserved.
