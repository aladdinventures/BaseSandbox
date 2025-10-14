# 📚 Shared Libraries / کتابخانه‌های مشترک

## Overview / نمای کلی

This directory contains shared libraries, utilities, and reusable components that can be used across multiple applications in the Aladdin Monorepo.

این پوشه شامل کتابخانه‌های مشترک، ابزارها و کامپوننت‌های قابل استفاده مجدد است که در چندین اپلیکیشن در Aladdin Monorepo قابل استفاده هستند.

## Structure / ساختار

Libraries should be organized by functionality:

```
libs/
├── utils/          # General utility functions
├── api/            # API client libraries
├── database/       # Database helpers and models
├── validation/     # Input validation utilities
└── logging/        # Logging and monitoring utilities
```

## Guidelines / راهنماها

### Creating a New Library / ایجاد کتابخانه جدید

1. Create a new directory with a descriptive name
2. Add a `README.md` explaining the library's purpose
3. Include a `requirements.txt` or `package.json` for dependencies
4. Write comprehensive tests
5. Document all public APIs

### Using a Library / استفاده از کتابخانه

```python
# Example: Using a shared utility
from libs.utils.validators import validate_email

if validate_email(user_email):
    # Process email
    pass
```

## Best Practices / بهترین روش‌ها

- Keep libraries **focused** and **single-purpose**
- Write **comprehensive tests** for all libraries
- Maintain **backward compatibility** when updating
- Use **semantic versioning** for library versions
- Document all **breaking changes**

---

**Note**: This directory is currently empty. Libraries will be added as common patterns emerge from application development.

**توجه**: این پوشه در حال حاضر خالی است. کتابخانه‌ها با ظهور الگوهای مشترک از توسعه اپلیکیشن اضافه خواهند شد.

