# 🧞 Aladdin Monorepo v2

[![CI/CD Pipeline](https://github.com/aladdinventures/aladdin-sandbox/actions/workflows/ci.yml/badge.svg)](https://github.com/aladdinventures/aladdin-sandbox/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview / نمای کلی

Welcome to the **Aladdin Monorepo v2** - a modular, scalable, and CI/CD-ready architecture for all Aladdin projects. This repository is designed to support automated testing with **MAMOS (Modular Autonomous Manager of Systems)** and multi-environment deployment (test, staging, production).

به **Aladdin Monorepo v2** خوش آمدید - یک معماری ماژولار، مقیاس‌پذیر و آماده برای CI/CD برای تمام پروژه‌های Aladdin. این ریپوزیتوری برای پشتیبانی از تست خودکار با **MAMOS (مدیر خودکار ماژولار سیستم‌ها)** و استقرار چند محیطی (تست، استیجینگ، پروداکشن) طراحی شده است.

## 🚀 Quick Start / شروع سریع

```bash
# Clone the repository
git clone https://github.com/aladdinventures/aladdin-sandbox.git
cd aladdin-sandbox

# View the structure documentation
cat README_STRUCTURE.md

# Install dependencies for a specific app
cd apps/backend
pip install -r requirements.txt

# Run the application
python app.py
```

## 📁 Repository Structure / ساختار ریپوزیتوری

```
aladdin-sandbox/
├── apps/           # Application projects
├── libs/           # Shared libraries
├── infra/          # Infrastructure & CI/CD
├── config/         # Configuration files
├── reports/        # Test reports
└── docs/           # Documentation
```

For detailed structure documentation, see [README_STRUCTURE.md](README_STRUCTURE.md).

برای مستندات کامل ساختار، فایل [README_STRUCTURE.md](README_STRUCTURE.md) را مشاهده کنید.

## 🎯 Key Features / ویژگی‌های کلیدی

- **Modular Architecture**: Organized project structure with clear separation of concerns
- **Automated Testing**: MAMOS-powered intelligent testing and reporting
- **CI/CD Ready**: GitHub Actions workflows for continuous integration and deployment
- **Multi-Environment Support**: Test, staging, and production environments
- **Bilingual Documentation**: English and Persian documentation throughout

## 📦 Projects / پروژه‌ها

### Backend API
Flask-based API service for pricing estimation and lead collection.

**Location**: `apps/backend/`  
**Tech Stack**: Python 3.11, Flask, SQLite  
**Endpoints**: `/estimate`, `/collect-lead`

### Frontend Web App
Static web application for user interface.

**Location**: `apps/frontend/`  
**Tech Stack**: HTML, CSS, JavaScript

### Integrations
External service integrations including Airtable and Calendly.

**Location**: `apps/integrations/`  
**Services**: Airtable API, Calendly API

### GPT Agent
GPT Agent configuration and OpenAPI specifications.

**Location**: `apps/gpt_agent/`

## 🔄 CI/CD Pipeline / پایپ‌لاین CI/CD

The repository uses GitHub Actions for automated testing and deployment:

1. **Trigger**: Push or Pull Request to `main` branch
2. **Testing**: MAMOS runs automated tests on all projects
3. **Reporting**: Bilingual Markdown reports generated
4. **Deployment**: Automatic deployment to configured environments

این ریپوزیتوری از GitHub Actions برای تست و استقرار خودکار استفاده می‌کند.

## 🧪 Testing with MAMOS / تست با MAMOS

MAMOS (Modular Autonomous Manager of Systems) is an AI-powered testing agent that:

- Automatically discovers and tests all projects
- Generates comprehensive bilingual reports
- Monitors deployment health
- Provides intelligent recommendations

MAMOS (مدیر خودکار ماژولار سیستم‌ها) یک عامل تست مبتنی بر هوش مصنوعی است که به صورت خودکار پروژه‌ها را کشف و تست می‌کند.

## 🛠️ Development / توسعه

### Adding a New Project / افزودن پروژه جدید

1. Create a new directory under `apps/`
2. Add project metadata to `config/projects.yaml`
3. Implement required commands (build, test, start)
4. Submit a pull request

### Running Tests Locally / اجرای تست‌ها به صورت محلی

```bash
# Run MAMOS locally
python infra/ci-cd/mamos_runner.py
```

## 📊 Monitoring & Reports / نظارت و گزارش‌ها

Test reports and deployment logs are stored in the `reports/` directory. MAMOS generates:

- **summary.md**: Overall test results
- **details/*.md**: Detailed reports for each project

گزارش‌های تست و لاگ‌های استقرار در پوشه `reports/` ذخیره می‌شوند.

## 🔐 Security / امنیت

- Environment variables are managed via GitHub Secrets
- Deployment protection rules enforced via GitHub Environments
- Required reviewers for production deployments
- Branch protection rules on `main` branch

## 📝 Contributing / مشارکت

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`feature/your-feature`)
3. Commit your changes with clear messages
4. Ensure all tests pass
5. Submit a pull request

## 📄 License / مجوز

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support / پشتیبانی

For questions, issues, or support:

- **GitHub Issues**: [Create an issue](https://github.com/aladdinventures/aladdin-sandbox/issues)
- **Documentation**: See `docs/` directory
- **Email**: support@aladdinventures.com

---

**Maintained by**: Aladdin Ventures Team  
**Version**: 2.0.0  
**Last Updated**: 2025-10-14

