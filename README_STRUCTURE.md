# 🏗️ Aladdin Monorepo v2 - Structure Documentation

## Overview / نمای کلی

This document describes the structure and organization of the Aladdin Monorepo v2. The repository is designed to support modular, scalable, and automated CI/CD-ready architecture for all Aladdin projects.

این سند ساختار و سازماندهی Aladdin Monorepo v2 را توضیح می‌دهد. این ریپوزیتوری برای پشتیبانی از معماری ماژولار، مقیاس‌پذیر و آماده برای CI/CD خودکار طراحی شده است.

## 📁 Directory Structure / ساختار پوشه‌ها

```
aladdin-sandbox/
├── apps/                    # Application projects / پروژه‌های اپلیکیشن
│   ├── backend/            # Backend API service
│   ├── frontend/           # Frontend web application
│   ├── integrations/       # Integration services (Airtable, Calendly, etc.)
│   └── gpt_agent/          # GPT Agent configuration
├── libs/                    # Shared libraries and utilities / کتابخانه‌های مشترک
├── infra/                   # Infrastructure and DevOps / زیرساخت و DevOps
│   └── ci-cd/              # CI/CD scripts and configurations
├── config/                  # Configuration files / فایل‌های پیکربندی
│   └── projects.yaml       # Project metadata for MAMOS
├── reports/                 # Test and deployment reports / گزارش‌های تست و استقرار
├── docs/                    # Documentation / مستندات
├── .github/                 # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline configuration
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── LICENSE                 # Project license
├── README.md               # Main project README
├── README_STRUCTURE.md     # This file
└── render.yaml             # Render deployment configuration
```

## 📦 Directory Descriptions / توضیحات پوشه‌ها

### `/apps` - Applications

Contains all deployable application projects. Each application is self-contained with its own dependencies and configuration.

شامل تمام پروژه‌های اپلیکیشن قابل استقرار است. هر اپلیکیشن مستقل با وابستگی‌ها و پیکربندی خاص خود است.

**Current Projects:**
- **backend**: Flask-based API service for pricing estimation and lead collection
- **frontend**: Static web application for user interface
- **integrations**: External service integrations (Airtable, Calendly)
- **gpt_agent**: GPT Agent instructions and OpenAPI specifications

### `/libs` - Shared Libraries

Reusable code, utilities, and shared components that can be used across multiple applications.

کدهای قابل استفاده مجدد، ابزارها و کامپوننت‌های مشترک که در چندین اپلیکیشن قابل استفاده هستند.

### `/infra` - Infrastructure

Infrastructure as Code (IaC) and DevOps tooling.

زیرساخت به عنوان کد (IaC) و ابزارهای DevOps.

**Subdirectories:**
- **ci-cd**: CI/CD scripts including MAMOS runner and automation tools

### `/config` - Configuration

Centralized configuration files for the entire monorepo.

فایل‌های پیکربندی متمرکز برای کل monorepo.

**Key Files:**
- **projects.yaml**: Project metadata for MAMOS automated testing

### `/reports` - Reports

Generated test reports, deployment logs, and MAMOS analysis results.

گزارش‌های تست تولید شده، لاگ‌های استقرار و نتایج تحلیل MAMOS.

### `/docs` - Documentation

Project documentation, guides, and technical specifications.

مستندات پروژه، راهنماها و مشخصات فنی.

## 🏷️ Naming Conventions / قراردادهای نام‌گذاری

### Project Names / نام پروژه‌ها

- Use **lowercase** with **hyphens** for directory names: `my-project-name`
- از **حروف کوچک** با **خط تیره** برای نام پوشه‌ها استفاده کنید: `my-project-name`

### File Names / نام فایل‌ها

- Python files: `snake_case.py` (e.g., `mamos_runner.py`)
- Configuration files: `lowercase.yaml` or `lowercase.json`
- Documentation: `UPPERCASE_WITH_UNDERSCORES.md` for root-level docs

### Branch Names / نام شاخه‌ها

- Main branch: `main`
- Feature branches: `feature/description`
- Bug fixes: `fix/description`
- Releases: `release/v1.0.0`

## 🔄 Workflow / جریان کاری

1. **Development**: Work in feature branches under `/apps` or `/libs`
2. **Testing**: MAMOS automatically tests changes via CI/CD pipeline
3. **Review**: Pull requests require review before merging to `main`
4. **Deployment**: Automated deployment to test/staging/production environments

## 🚀 Getting Started / شروع کار

### Prerequisites / پیش‌نیازها

- Python 3.11+
- Node.js 18+ (for frontend projects)
- Git
- GitHub CLI (optional)

### Setup / راه‌اندازی

```bash
# Clone the repository
git clone https://github.com/aladdinventures/aladdin-sandbox.git
cd aladdin-sandbox

# Install dependencies (example for backend)
cd apps/backend
pip install -r requirements.txt

# Run the application
python app.py
```

## 📊 Project Metadata / متادیتای پروژه

Each project in `/apps` should have the following metadata defined in `config/projects.yaml`:

- **name**: Project identifier
- **path**: Relative path from repository root
- **framework_type**: Technology stack (e.g., Flask, React, Node.js)
- **build_command**: Command to build the project
- **test_command**: Command to run tests
- **start_command**: Command to start the application
- **health_checks**: Endpoints or scripts to verify application health

## 🔐 Security / امنیت

- **Never commit** `.env` files or secrets to the repository
- Use GitHub Secrets for sensitive environment variables
- Follow the principle of least privilege for access control
- Use GitHub Environments for deployment protection rules

## 📝 Contributing / مشارکت

1. Create a feature branch from `main`
2. Make your changes following the naming conventions
3. Ensure all tests pass locally
4. Submit a pull request with a clear description
5. Wait for MAMOS automated testing and review

## 📞 Support / پشتیبانی

For questions or issues, please refer to the main project documentation or contact the development team.

---

**Last Updated**: 2025-10-14  
**Version**: 2.0.0  
**Maintained by**: Aladdin Ventures Team

