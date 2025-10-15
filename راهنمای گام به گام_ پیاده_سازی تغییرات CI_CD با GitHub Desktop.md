## راهنمای گام به گام: پیاده‌سازی تغییرات CI/CD با GitHub Desktop

این راهنما به شما کمک می‌کند تا تغییرات CI/CD را که شامل یکپارچه‌سازی Render و مکانیزم ولیدیشن است، با استفاده از GitHub Desktop به صورت ایمن و کنترل شده در مخزن `Aladdin-sandbox` پیاده‌سازی کنید.

### پیش‌نیازها:

1.  **GitHub Desktop**: اطمینان حاصل کنید که GitHub Desktop بر روی سیستم شما نصب شده است.
2.  **فایل زیپ تغییرات**: فایل `aladdin-monorepo-with-integrated-validation.zip` را که قبلاً به شما تحویل داده شد، دانلود و در یک پوشه موقت از حالت فشرده خارج کنید.
3.  **دسترسی به مخزن GitHub**: شما باید دسترسی لازم برای Push کردن به مخزن و ایجاد Pull Request در GitHub را داشته باشید.

### مراحل:

#### گام 1: کلون کردن مخزن (اگر قبلاً انجام نداده‌اید)

1.  **GitHub Desktop را باز کنید.**
2.  اگر مخزن `Aladdin-sandbox` قبلاً در GitHub Desktop شما نیست:
    *   روی `File` -> `Clone Repository...` کلیک کنید.
    *   در تب `URL`، آدرس مخزن خود را وارد کنید: `https://github.com/aladdinventures/aladdin-sandbox`
    *   یک مسیر محلی برای ذخیره مخزن انتخاب کنید و روی `Clone` کلیک کنید.

#### گام 2: ایجاد یک برنچ فرعی جدید

1.  در GitHub Desktop، مطمئن شوید که مخزن `Aladdin-sandbox` انتخاب شده است.
2.  در بالای صفحه، روی دکمه `Current Branch` (که معمولاً `main` یا `master` را نشان می‌دهد) کلیک کنید.
3.  روی `New Branch...` کلیک کنید.
4.  یک نام معنی‌دار برای برنچ خود وارد کنید، مثلاً `feature/ci-cd-render-validation`.
5.  مطمئن شوید که `Branch from` روی `main` (یا برنچ اصلی توسعه شما) تنظیم شده باشد.
6.  روی `Create Branch` کلیک کنید.

#### گام 3: اعمال تغییرات از فایل زیپ

1.  به پوشه محلی مخزن `Aladdin-sandbox` که در گام 1 کلون کردید، بروید.
2.  پوشه `aladdin-sandbox` را از داخل فایل زیپ `aladdin-monorepo-with-integrated-validation.zip` که از حالت فشرده خارج کرده‌اید، باز کنید.
3.  **تمامی محتویات** این پوشه `aladdin-sandbox` (شامل پوشه‌های `.github`, `apps`, `config`, `infra` و غیره) را کپی کرده و در پوشه ریشه مخزن محلی `Aladdin-sandbox` خود **جایگذاری (Overwrite)** کنید. این کار فایل‌های موجود را با نسخه‌های جدید به‌روزرسانی می‌کند و فایل‌های جدید را اضافه می‌کند.

#### گام 4: کامیت کردن تغییرات

1.  به GitHub Desktop بازگردید.
2.  اکنون باید لیستی از فایل‌های تغییر یافته را در پنل سمت چپ مشاهده کنید.
3.  در پایین پنل سمت چپ، یک پیام کامیت (Commit Message) معنی‌دار وارد کنید، مثلاً: `feat: Integrate Render deployment, manual approval, and CI/CD validation`
4.  می‌توانید یک توضیح (Description) اختیاری نیز اضافه کنید.
5.  روی دکمه `Commit to feature/ci-cd-render-validation` (یا نام برنچ شما) کلیک کنید.

#### گام 5: Push کردن برنچ به GitHub

1.  پس از کامیت، دکمه `Publish Branch` در بالای GitHub Desktop ظاهر می‌شود. روی آن کلیک کنید.
2.  این کار برنچ جدید شما را به مخزن راه دور (Remote Repository) در GitHub Push می‌کند.

#### گام 6: ایجاد Pull Request (PR)

1.  پس از Push موفقیت‌آمیز، GitHub Desktop ممکن است به شما پیشنهاد دهد که یک Pull Request ایجاد کنید. روی `Create Pull Request` کلیک کنید.
2.  اگر این گزینه ظاهر نشد، به صفحه مخزن خود در GitHub.com بروید. معمولاً یک بنر سبز رنگ در بالای صفحه ظاهر می‌شود که به شما پیشنهاد ایجاد PR از برنچ جدیدتان را می‌دهد. روی `Compare & pull request` کلیک کنید.
3.  در صفحه Pull Request:
    *   مطمئن شوید که برنچ `base` روی `main` (یا برنچ اصلی توسعه شما) و برنچ `compare` روی برنچ فرعی شما (`feature/ci-cd-render-validation`) تنظیم شده باشد.
    *   عنوان و توضیحات PR را بررسی کنید. می‌توانید جزئیات بیشتری در مورد تغییرات CI/CD اضافه کنید.
    *   روی `Create pull request` کلیک کنید.

#### گام 7: پیکربندی دستی پیش‌نیازها در GitHub و Render (بسیار مهم!)

**این گام‌ها را باید در رابط کاربری GitHub و Render انجام دهید و برای عملکرد صحیح CI/CD حیاتی هستند:**

1.  **در GitHub.com:**
    *   **مجوزهای GitHub App (Manus Connector) را تنظیم کنید**: اطمینان حاصل کنید که GitHub App (Manus Connector) دارای مجوز `Read and write` برای `Workflows` در تنظیمات مخزن شما باشد (`Settings` -> `Developer settings` -> `GitHub Apps` -> `Manus Connector` -> `Permissions & events`).
    *   **محیط‌های GitHub (Environments) را پیکربندی کنید**: محیط‌های `Test`, `Staging`, و `Production` را در تنظیمات مخزن خود (`Settings` -> `Environments`) ایجاد و پیکربندی کنید. **برای محیط‌های `Staging` و `Production`، گزینه `Required reviewers` را فعال کنید و تیم‌ها یا کاربرانی را که باید استقرارها را تأیید کنند، تعیین نمایید.**
    *   **GitHub Secrets را تنظیم کنید**: Render API Key را که از Render.com دریافت کرده‌اید، به عنوان GitHub Secret در مخزن خود (یا در سطح هر Environment) ذخیره کنید. نام این Secretها باید با `render_api_key_secret_name` که در `config/projects.yaml` و فایل‌های Workflow مشخص شده‌اند، مطابقت داشته باشند (مثلاً `RENDER_BACKEND_TEST_API_KEY`).
2.  **در Render.com:**
    *   برای هر پروژه (backend, frontend, integrations, gpt_agent, youtube_automation, ai_newsbot, mamos-dashboard, mamos-orchestrator) و برای هر محیط (Test, Staging, Production) یک سرویس (Service) جداگانه ایجاد کنید.
    *   **شناسه سرویس (Service ID)** هر یک از این سرویس‌ها را یادداشت کنید و اطمینان حاصل کنید که با مقادیر `render_service_id` در فایل `config/projects.yaml` مطابقت دارند.

#### گام 8: تست و نظارت بر Workflowها

1.  پس از ایجاد Pull Request، GitHub Actions به طور خودکار Workflowهای CI/CD را بر روی برنچ فرعی شما اجرا می‌کند.
2.  به تب `Actions` در مخزن GitHub خود بروید.
3.  Workflow مربوط به برنچ فرعی خود را پیدا کنید و روی آن کلیک کنید.
4.  می‌توانید مراحل `validate`, `build-and-test` و `deploy-test` را مشاهده کنید که باید به صورت خودکار اجرا شوند.
5.  هنگامی که Workflow به مرحله `deploy-staging` یا `deploy-production` می‌رسد، متوقف شده و منتظر تأیید دستی شما (یا Reviewerهای تعیین شده) می‌ماند. در لاگ‌های این مرحله، پیام‌های راهنمای انگلیسی که ما اضافه کردیم، نمایش داده می‌شوند و پیش‌نیازها را یادآوری می‌کنند.
6.  پس از بررسی و اطمینان از صحت عملکرد، می‌توانید استقرار را تأیید کنید.

#### گام 9: ادغام (Merge) Pull Request

1.  پس از اینکه تمامی Workflowها با موفقیت اجرا شدند و شما از عملکرد صحیح آن‌ها اطمینان حاصل کردید، می‌توانید Pull Request را ادغام کنید.
2.  در صفحه Pull Request در GitHub، روی دکمه `Merge pull request` کلیک کنید.
3.  این کار تغییرات را از برنچ فرعی شما به برنچ اصلی (`main`) منتقل می‌کند.
4.  پس از ادغام، می‌توانید برنچ فرعی خود را حذف کنید.

با دنبال کردن این مراحل، شما با موفقیت سیستم CI/CD جدید را در مخزن خود پیاده‌سازی کرده‌اید. اگر در هر مرحله‌ای با مشکلی مواجه شدید، لطفاً سوال بپرسید.
