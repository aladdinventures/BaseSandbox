# AI_NewsBot_Aladdin Research Report

## 1. Project Overview and Goal

The AI_NewsBot_Aladdin project aims to develop an AI-powered NewsBot that automates the monitoring of various online sources (websites, documents, repositories, project updates) and generates concise, high-quality posts for social media platforms like LinkedIn, Instagram, and Twitter (X). The ultimate goal is to streamline content creation and dissemination for Aladdin Ventures / CI-CD Aladdin Trading, with future phases incorporating automation for scheduling and publishing these posts via connected APIs.

## 2. Technical Understanding

### 2.1. Input → Process → Output Flow

Given the absence of the base Python script, the following flow is conceptualized based on the project description:

**Input:**
*   **Sources:** URLs of websites, paths to local documents, repository URLs, and project update feeds to be monitored.
*   **Monitoring Frequency:** Configurable schedules for checking updates (e.g., daily, hourly).

**Process:**
1.  **Change Detection:** The system periodically accesses the configured sources. For websites and documents, this involves fetching content. For repositories, it might involve checking commit histories or file changes. A hash-based comparison (e.g., MD5 or SHA256 of content/state) is used to identify new or modified content.
2.  **Content Extraction & Pre-processing:** Upon detecting changes, relevant content is extracted. This may involve web scraping, parsing document formats (PDF, DOCX), or reading repository commit messages/file diffs. The extracted content is then cleaned and formatted for AI processing.
3.  **AI Summarization & Generation:** The pre-processed content is fed into an AI model (e.g., OpenAI API or a local LLM). The AI is prompted to summarize the changes or key information and generate short, engaging social media posts tailored for LinkedIn, Instagram, and Twitter (X). The posts are specifically requested to be in Persian.

**Output:**
*   **Generated Posts:** The AI-generated social media posts (in Persian) are saved into designated local folders, categorized by social media platform (e.g., `output/linkedin/`, `output/instagram/`, `output/twitter/`).
*   **Metadata:** Associated metadata such as source URL, detection timestamp, and original content hash might also be stored alongside the posts.

### 2.2. AI Summarization and Generation Triggering

Based on the project description, the AI summarization and generation process is triggered **conditionally** upon the detection of new or updated content from the monitored sources. The workflow would likely be:

1.  **Scheduled Scan:** A scheduler initiates a scan of all configured sources.
2.  **Change Identified:** The change detection module identifies a significant update (e.g., new article, code commit, document revision).
3.  **Content Prepared:** The new/changed content is extracted and prepared for the AI model.
4.  **AI Invocation:** An API call is made to the AI model (e.g., OpenAI API) with the prepared content and a specific prompt instructing it to summarize and generate social media posts in Persian for the target platforms. For local models, a similar invocation would occur against the locally hosted model API.
5.  **Post Storage:** The AI's response, containing the generated posts, is then parsed and saved to the local file system.

### 2.3. Detection of Changes (Hash Diff)

The detection of changes using a hash diff mechanism is a robust way to identify modifications efficiently. The general process would involve:

1.  **Initial Scan & Hashing:** When a source is first added or at the initial scan, its content is fetched, and a cryptographic hash (e.g., SHA256) of its relevant data (e.g., webpage HTML, document text, repository commit hash) is computed and stored in a database or file.
2.  **Subsequent Scans:** In subsequent scans, the content of the source is fetched again, and a new hash is computed.
3.  **Comparison:** The newly computed hash is compared with the previously stored hash. If the hashes differ, a change is detected.
4.  **Update Stored Hash:** If a change is detected, the new hash replaces the old one in storage to reflect the current state.

This method avoids storing the entire content of sources, making the change detection process lightweight and scalable. For repositories, this could involve tracking the latest commit hash of a specific branch.


## 3. Proposed Architecture for Scalable Automation

To ensure scalability, maintainability, and efficient resource utilization, the AI_NewsBot_Aladdin project should adopt a modular, microservices-oriented architecture. This approach allows for independent development, deployment, and scaling of different components.

### 3.1. Modularization into Services

The current script logic can be modularized into distinct services, each responsible for a specific function:

*   **Crawler Service:**
    *   **Functionality:** Responsible for monitoring and fetching content from various sources (websites, documents, repositories).
    *   **Inputs:** List of sources to monitor, monitoring frequency.
    *   **Outputs:** Raw content from sources, detected changes.
    *   **Technologies:** Python with libraries like `requests`, `BeautifulSoup` for web scraping; `GitPython` for repository monitoring; document parsing libraries (e.g., `python-docx`, `PyPDF2`).

*   **Change Detection Service:**
    *   **Functionality:** Compares fetched content with previously stored states to identify new or updated information using hash diffing.
    *   **Inputs:** Raw content from Crawler Service, historical content hashes.
    *   **Outputs:** Notification of changes, extracted relevant content.
    *   **Technologies:** Python, potentially a dedicated database for storing content hashes and metadata.

*   **Summarizer & Generator Service:**
    *   **Functionality:** Takes extracted content, summarizes it, and generates social media posts in Persian for target platforms using AI models.
    *   **Inputs:** Extracted content from Change Detection Service.
    *   **Outputs:** AI-generated social media posts (Persian).
    *   **Technologies:** Python, OpenAI API client, or local LLM inference server client (e.g., `llama-cpp-python` for LLaMA/Ollama).

*   **Publisher Service:**
    *   **Functionality:** Manages the storage of generated posts for manual review and, in later phases, handles automated publishing to social media platforms via their respective APIs.
    *   **Inputs:** AI-generated social media posts.
    *   **Outputs:** Stored posts, (future) published posts.
    *   **Technologies:** Python, file system operations, (future) social media API clients (LinkedIn API, Instagram Graph API, Twitter API).

### 3.2. Queue / Scheduler Setup

To manage asynchronous tasks, handle varying loads, and ensure reliable processing, a robust queue and scheduler system is essential.

*   **Scheduler:** For periodic tasks (e.g., initiating crawls, checking for changes), a scheduler like **Celery Beat** (with Redis or RabbitMQ as a message broker) or a simple `cron` job manager can be used. Celery Beat is preferred for its integration with Celery workers.

*   **Message Queue:** **Redis** or **RabbitMQ** can serve as the message broker for inter-service communication. When the Crawler Service fetches new content, it can push a message to a queue. The Change Detection Service consumes this message, processes it, and pushes another message to a summarization queue, and so on. This decouples services and allows for independent scaling.

    *   **Example Flow:**
        1.  Scheduler triggers Crawler Service.
        2.  Crawler Service fetches data and publishes a message to `raw_content_queue`.
        3.  Change Detection Service consumes from `raw_content_queue`, processes, and publishes to `changed_content_queue`.
        4.  Summarizer & Generator Service consumes from `changed_content_queue`, processes, and publishes to `generated_posts_queue`.
        5.  Publisher Service consumes from `generated_posts_queue` and saves posts locally.

### 3.3. Recommended Database and File Structure

*   **Database:** A **PostgreSQL** database is recommended for storing structured data due to its robustness, scalability, and rich feature set. It can store:
    *   **Source Configuration:** URLs, document paths, repository details, monitoring frequency.
    *   **Content Hashes:** Historical hashes for change detection, along with timestamps.
    *   **Generated Post Metadata:** Details about generated posts (e.g., source, date, target platform, status).
    *   **User Preferences:** (Future) User-specific settings for post generation or publishing.

*   **File Structure:**
    *   **Output Storage:** Generated posts should be stored in a well-organized local file system structure, as specified:
        ```
        /output
        ├── linkedin/
        │   ├── post_1.md
        │   └── post_2.md
        ├── instagram/
        │   ├── post_3.md
        │   └── post_4.md
        └── twitter/
            ├── post_5.md
            └── post_6.md
        ```
    *   **Configuration Files:** `.env` files for environment variables and API keys (for development/testing) or a more secure solution like HashiCorp Vault for production.
    *   **Logs:** A dedicated directory for service logs.

### 3.4. Integration with OpenAI API and Future Local Models

The Summarizer & Generator Service should be designed with an **abstraction layer** to easily switch between different AI models.

*   **OpenAI API Integration:** Initially, the service will integrate with the OpenAI API (e.g., `gpt-4.1-mini`, `gpt-4.1-nano`, `gemini-2.5-flash` as per environment variables) using the `openai` Python client. API keys should be securely managed.

*   **Local Models (LLaMA or Ollama):** For future integration with local models, the abstraction layer will allow swapping the OpenAI client with a client for the chosen local model. This might involve:
    *   **Ollama:** Running Ollama locally to serve various open-source models (LLaMA, Mistral, etc.) via a compatible API endpoint. The Summarizer & Generator Service would then make requests to this local endpoint.
    *   **Direct LLaMA Integration:** Using libraries like `llama-cpp-python` to run LLaMA models directly within the service, though this requires significant computational resources.

This modular approach ensures that the system can evolve, incorporate new AI models, and scale components independently as the project grows.


## 4. Identified Risks and Constraints

Developing the AI_NewsBot_Aladdin involves several potential risks and constraints that need to be carefully considered and mitigated.

### 4.1. Rate Limits for Social APIs

Social media platforms impose **rate limits** on API requests to prevent abuse and ensure fair usage. Exceeding these limits can lead to temporary bans or permanent suspension of API access. This is a critical concern for automated posting.

*   **LinkedIn API:** LinkedIn has various rate limits depending on the type of API call (e.g., sharing, profile access). These limits are often dynamic and can change without much notice. Exceeding them can result in `429 Too Many Requests` errors.
*   **Meta Graph API (Instagram):** Instagram's API, accessed via the Meta Graph API, also has rate limits based on a rolling 24-hour window and per-app/per-user limits. Publishing content frequently can quickly hit these caps.
*   **Twitter (X) API:** The Twitter API (now X API) has stringent rate limits, especially for free and basic tiers. These limits apply to posting, reading timelines, and other actions. High-volume automated posting will likely require a paid tier subscription.

**Mitigation Strategies:**
*   **Implement Exponential Backoff and Retry Mechanisms:** When a rate limit error is encountered, the system should wait for an increasing amount of time before retrying the request.
*   **Distributed Posting:** If possible, distribute posting across multiple accounts or applications (if allowed by platform terms of service) to increase overall throughput.
*   **Monitor API Usage:** Implement monitoring and alerting for API usage to proactively identify when limits are being approached.
*   **Tiered API Access:** Plan for upgrading to higher-tier API access for social media platforms as the bot's usage scales.

### 4.2. OpenAI API Cost and Token Optimization

Using large language models like OpenAI's incurs costs based on **token usage** (both input and output tokens). Inefficient prompting or excessive generation can quickly lead to high operational expenses.

*   **Cost per Token:** Different models have different pricing structures per token. Selecting the most cost-effective model for a given task (e.g., `gpt-4.1-mini` for simpler summarization) is crucial.
*   **Prompt Engineering:** The way prompts are constructed directly impacts token usage. Concise and effective prompts reduce input tokens. Instructing the model to generate only necessary information reduces output tokens.
*   **Context Window Management:** For long documents, summarizing in chunks or using techniques like RAG (Retrieval Augmented Generation) can help manage the context window and reduce token count.

**Mitigation Strategies:**
*   **Prompt Optimization:** Continuously refine prompts to be as efficient as possible, minimizing unnecessary words while retaining clarity and effectiveness.
*   **Model Selection:** Dynamically select the appropriate AI model based on the complexity and length of the content to be processed.
*   **Caching:** Cache summaries or generated posts for content that has not changed to avoid reprocessing and re-generating.
*   **Token Usage Monitoring:** Implement detailed logging and monitoring of token usage to track costs and identify areas for optimization.
*   **Local Model Exploration:** As identified in the project overview, exploring local models (LLaMA, Ollama) can significantly reduce or eliminate API costs, especially for high-volume tasks, once they reach a comparable quality level.

### 4.3. Security and Storage of API Keys

API keys for OpenAI and social media platforms are sensitive credentials that grant access to external services. Their compromise can lead to unauthorized usage, data breaches, and significant financial or reputational damage.

*   **Vulnerability:** Storing API keys directly in code or in `.env` files that are committed to version control is a major security risk.
*   **Access Control:** Ensuring that only authorized components and personnel have access to these keys is vital.

**Mitigation Strategies:**
*   **Environment Variables:** For development and testing, API keys should be loaded from environment variables, not hardcoded.
*   **Secrets Management Service:** For production deployments, a dedicated secrets management service like **HashiCorp Vault**, AWS Secrets Manager, or Google Secret Manager should be used. These services provide secure storage, access control, and auditing for sensitive credentials.
*   **Principle of Least Privilege:** API keys should only have the minimum necessary permissions required for their function.
*   **Regular Rotation:** API keys should be rotated periodically to minimize the impact of a potential compromise.

### 4.4. GDPR/Privacy and Company Data Handling Rules

When monitoring websites and documents, especially those containing personal or sensitive information, compliance with data protection regulations like GDPR (General Data Protection Regulation) and internal company data handling rules is paramount.

*   **Data Collection:** The bot might inadvertently collect personal data from monitored sources.
*   **Data Storage:** Storing collected data, even temporarily, requires adherence to privacy principles.
*   **Consent and Transparency:** If the bot interacts with user-generated content or platforms, considerations around consent and transparency become relevant.

**Mitigation Strategies:**
*   **Data Minimization:** Only collect and process data that is strictly necessary for generating news posts. Implement filters to exclude personal identifiable information (PII).
*   **Data Anonymization/Pseudonymization:** Where possible, anonymize or pseudonymize data before storage or processing.
*   **Secure Data Storage:** Ensure that any collected data is stored securely, encrypted at rest and in transit.
*   **Compliance Audit:** Conduct regular audits to ensure compliance with GDPR and internal data handling policies.
*   **Legal Counsel:** Consult with legal counsel to ensure the bot's operations fully comply with relevant data protection laws and company policies, especially concerning international data transfers if applicable.

Addressing these risks and constraints proactively will contribute to the long-term success and sustainability of the AI_NewsBot_Aladdin project.


## 5. Proposed CI/CD Integration for Aladdin-sandbox

Integrating the AI_NewsBot_Aladdin into the existing `aladdin-sandbox` repository requires careful consideration of deployment, integration points, folder conventions, and automated build/release triggers. The goal is to leverage the existing CI/CD pipeline to ensure seamless development and deployment.

### 5.1. Deployment within `aladdin-sandbox`

The `AI_NewsBot_Aladdin` project should be deployed as a new application within the `aladdin-sandbox` repository. Following the established convention, it should reside in its own subfolder under `aladdin-sandbox/apps/`.

*   **Recommended Location:** `/aladdin-sandbox/apps/ai_newsbot/`
*   **Internal Structure:** Within this `ai_newsbot` directory, the project can have its own `src/`, `config/`, `tests/`, and `docs/` folders, maintaining modularity and separation of concerns.

This placement ensures that the NewsBot is treated as a distinct application within the Aladdin ecosystem, benefiting from the sandbox's existing infrastructure and CI/CD workflows.

### 5.2. Integration Points with Aladdin Docs & Dashboard

For effective management and visibility, the AI_NewsBot_Aladdin needs to integrate with Aladdin Docs and Dashboard modules.

*   **Aladdin Docs Integration:**
    *   **Research Report:** The current research report (`AI_NewsBot_Aladdin_Research_Report.md`) should be placed in `/aladdin-sandbox/docs/research/ai_newsbot/` as specified. This makes the foundational documentation accessible within the broader Aladdin documentation.
    *   **User Guides/API Documentation:** As the project progresses, user guides, API documentation for the NewsBot's internal services, and deployment instructions should also be integrated into the Aladdin Docs structure, potentially under `/aladdin-sandbox/docs/apps/ai_newsbot/`.

*   **Aladdin Dashboard Integration:**
    *   **Monitoring & Metrics:** The NewsBot's operational metrics (e.g., number of sources monitored, posts generated, API call success/failure rates, token usage) should be exposed via APIs that the Aladdin Dashboard can consume. This allows for centralized monitoring and performance tracking.
    *   **Configuration Management:** The Dashboard could potentially offer a UI for configuring NewsBot sources, monitoring frequencies, and reviewing generated posts before publishing.
    *   **Post Management:** A dedicated section in the Dashboard for reviewing, editing, approving, and scheduling NewsBot-generated posts would be a crucial integration point for Phase 3.

### 5.3. Folder Convention Suggestion

Adhering to a consistent folder convention is vital for maintainability and discoverability within a large repository like `aladdin-sandbox`.

*   **Application Code:** `/aladdin-sandbox/apps/ai_newsbot/`
    *   `src/`: Core Python code for the services (crawler, summarizer, etc.).
    *   `config/`: Service-specific configuration files.
    *   `tests/`: Unit and integration tests for the NewsBot.
    *   `scripts/`: Utility scripts (e.g., setup, data migration).
*   **Documentation:** `/aladdin-sandbox/docs/research/ai_newsbot/` (for research reports) and `/aladdin-sandbox/docs/apps/ai_newsbot/` (for user guides, API docs).
*   **Infrastructure (if specific to NewsBot):** `/aladdin-sandbox/infra/ai_newsbot/` (e.g., Dockerfiles, Kubernetes manifests, if not managed centrally).

### 5.4. How to Trigger Builds and Releases Automatically

The existing GitHub-based CI/CD release workflow can be extended to automatically build and release the AI_NewsBot_Aladdin.

*   **Version Control Trigger:** Any push to the `main` branch within the `/aladdin-sandbox/apps/ai_newsbot/` directory (or a designated release branch) should trigger the CI/CD pipeline.
*   **GitHub Actions/Workflows:**
    1.  **Linting & Testing:** The pipeline should first run linters (e.g., `flake8`, `pylint`) and unit/integration tests defined in `/aladdin-sandbox/apps/ai_newsbot/tests/`.
    2.  **Build Docker Image:** Upon successful testing, a Docker image for each NewsBot service (Crawler, Summarizer, etc.) should be built and tagged (e.g., `ai_newsbot-crawler:v1.0.0`). These images can then be pushed to a container registry (e.g., GitHub Container Registry, Docker Hub).
    3.  **Deployment Manifest Generation:** If using Kubernetes, updated deployment manifests (e.g., `deployment.yaml`, `service.yaml`) can be generated or updated to reference the new Docker image tags.
    4.  **Deployment:** The CI/CD pipeline can then trigger a deployment to the staging or production environment. This could involve applying Kubernetes manifests, updating `render.yaml` configurations, or executing deployment scripts.
    5.  **Documentation Update:** Automated generation and deployment of documentation (e.g., API docs) to Aladdin Docs upon code changes.
*   **Semantic Versioning:** Implement semantic versioning for the NewsBot application to clearly track changes and releases.
*   **Rollback Strategy:** Ensure the CI/CD pipeline supports easy rollback to previous stable versions in case of deployment issues.

By integrating the AI_NewsBot_Aladdin into the `aladdin-sandbox` CI/CD pipeline, the development team can benefit from automated quality checks, consistent deployments, and a streamlined release process.


## 6. Suggested Phase Roadmap for Implementation

To guide the development of the AI_NewsBot_Aladdin, a phased roadmap is proposed, building upon the research and architectural considerations outlined above. This roadmap aligns with the project overview and aims for iterative development and deployment.

### Phase 1: Research & Understanding (Current Phase)

*   **Objective:** Comprehensive understanding of project goals, technical requirements, potential risks, and architectural considerations.
*   **Key Activities:**
    *   Analyze project brief and user requirements.
    *   Document technical understanding (Input-Process-Output, AI triggering, change detection).
    *   Propose a scalable architecture (modular services, queue/scheduler, DB, file structure).
    *   Identify and document risks (API rate limits, OpenAI costs, security, GDPR).
    *   Propose CI/CD integration within `aladdin-sandbox`.
    *   Develop a phased implementation roadmap.
*   **Deliverable:** `AI_NewsBot_Aladdin_Research_Report.md` (this document).

### Phase 2: Development & Local Testing

*   **Objective:** Implement the core functionalities of the NewsBot, focusing on change detection, AI summarization/generation, and local post storage, ensuring all components are functional and testable in a local environment.
*   **Key Activities:**
    *   **Setup Project Structure:** Create the `/aladdin-sandbox/apps/ai_newsbot/` directory with `src/`, `config/`, `tests/` subdirectories.
    *   **Implement Crawler Service:** Develop modules for fetching content from specified sources (web, documents, basic repository monitoring).
    *   **Implement Change Detection Service:** Develop the hash-diffing mechanism to identify content changes and trigger subsequent processes.
    *   **Integrate AI Summarization & Generation:** Implement the service to call the OpenAI API (or a mock API for MVP) to summarize content and generate Persian social media posts.
    *   **Implement Local Publisher Service:** Develop functionality to save generated posts to the local file system in the specified output structure.
    *   **Develop Unit and Integration Tests:** Ensure robust testing for all developed modules.
    *   **Local Deployment & Testing:** Deploy and test the integrated services locally using Docker Compose or similar tools.
*   **Deliverables:**
    *   Functional core NewsBot application (Python code).
    *   Comprehensive test suite.
    *   Local deployment instructions.
    *   Initial documentation for developers.

### Phase 3: API Publishing & Automation

*   **Objective:** Extend the NewsBot to automatically publish approved posts to social media platforms via their respective APIs and implement a robust scheduling mechanism.
*   **Key Activities:**
    *   **Social Media API Integration:** Integrate the Publisher Service with LinkedIn, Instagram (Meta Graph API), and Twitter (X) APIs for automated posting.
    *   **Implement Scheduling:** Integrate Celery Beat/Celery workers for scheduling content monitoring and post publishing.
    *   **Post Approval Workflow:** Develop a mechanism (e.g., a simple web interface or CLI tool) for reviewing and approving AI-generated posts before automated publishing.
    *   **Error Handling & Logging:** Enhance error handling, retry mechanisms, and comprehensive logging for API interactions and publishing.
    *   **Secrets Management:** Implement secure handling of API keys using a secrets management solution.
*   **Deliverables:**
    *   Automated social media publishing capabilities.
    *   Robust scheduling system.
    *   Post approval interface/tool.
    *   Enhanced monitoring and logging.

### Phase 4: Analytics and Feedback Loop

*   **Objective:** Implement analytics to track post performance, gather feedback, and use this data to refine AI models and overall bot effectiveness.
*   **Key Activities:**
    *   **Performance Tracking:** Integrate with social media analytics APIs (if available) or track engagement metrics (likes, shares, comments) for published posts.
    *   **Feedback Mechanism:** Develop a system for collecting feedback on AI-generated post quality and effectiveness.
    *   **AI Model Refinement:** Use performance data and feedback to fine-tune AI prompts or models for better post generation.
    *   **Dashboard Integration:** Integrate key performance indicators (KPIs) and analytics into the Aladdin Dashboard.
    *   **Scalability Enhancements:** Optimize services for performance and cost based on real-world usage data.
*   **Deliverables:**
    *   Analytics and reporting features.
    *   Feedback collection system.
    *   Improved AI post generation quality.
    *   Comprehensive dashboard integration.
