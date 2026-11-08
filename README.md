# MUSE — AI-Powered Meme Marketing & Content Automation

### Transforming Products into Creative, AI-Generated Marketing Content

**MUSE** is an AI-powered marketing content generation platform designed to streamline the creation of engaging meme-based advertisements, short-form videos, and promotional content.

By combining large language models, retrieval-augmented generation (RAG), AI-assisted content creation, and workflow automation, MUSE provides an integrated approach to transforming product information into creative marketing concepts.

The platform features a modern web interface alongside a Python backend responsible for AI-driven idea generation, multimedia processing, and publishing workflows.

**Repository:** [github.com/Mashielkhan/Hack_submission](https://github.com/Mashielkhan/Hack_submission)

---

## Project Overview

Creating effective social media advertisements often involves multiple stages, including trend research, creative ideation, scriptwriting, media generation, editing, and publishing.

MUSE explores how artificial intelligence can simplify this process through an integrated content-generation workflow.

Users can provide product information and use AI-assisted workflows to develop marketing ideas based on relevant meme trends.

The application combines a React-based frontend with a Python backend structured around three main workflows:

1. **Meme Idea Generation** — Generate marketing concepts and scripts using AI and trend retrieval.
2. **Content Generation** — Process creative concepts through multimedia generation services.
3. **Publishing Workflow** — Coordinate prepared content for publishing.

The goal is to provide businesses, marketers, and content creators with a centralized environment for experimenting with AI-assisted advertising.

---

## Key Features

### 1. AI-Powered Meme Idea Generation

MUSE uses Mistral AI and LangGraph to transform product descriptions into creative meme advertisement ideas.

The idea-generation pipeline produces structured concepts containing:

- Meme concept title.
- Humorous advertisement narration.
- Detailed visual generation prompt.
- Product-relevant marketing context.

The workflow is designed to generate three concepts from each request.

### 2. Retrieval-Augmented Trend Research

The application uses vector-based retrieval to incorporate relevant meme trends into AI-generated marketing ideas.

**Components include:**

- ChromaDB for vector storage.
- Mistral AI embeddings for semantic representation.
- Local JSON-based trend information.
- Apify dataset integration for retrieving external trend data.
- Semantic retrieval to select relevant context.

This approach makes it possible to ground creative recommendations in stored trend information rather than relying entirely on an LLM's general knowledge.

### 3. AI-Assisted Content Generation

The backend includes a dedicated content-generation workflow implemented in `flow2_generate.py`.

Supporting utilities provide functionality for working with multimedia assets, including audio, video, and content stitching.

The modular architecture separates content generation from creative ideation.

### 4. Automated Publishing Workflow

MUSE includes a separate publishing workflow through `flow3_publish.py`.

This design provides a foundation for organizing content production and distribution.

Publishing capabilities and supported external platforms depend on the integrations configured in the backend.

### 5. Marketing Dashboard

The React frontend contains dedicated screens for navigating the application's marketing functionality.

The available page components include:

- Dashboard.
- Projects.
- Project details.
- Campaign management.
- Video Studio.
- Analytics.
- Application settings.

The interface is structured to provide a centralized environment for managing AI-assisted content workflows.

### 6. Modular AI Architecture

MUSE separates AI reasoning, multimedia operations, and user interface components.

This architecture helps keep individual services independently maintainable and supports future integration with additional AI providers.

---

## Technology Stack

| Layer                 | Technology            | Purpose                                |
| --------------------- | --------------------- | -------------------------------------- |
| Frontend              | React, TypeScript     | Web application interface              |
| Build Tool            | Vite                  | Development and frontend builds        |
| Styling               | Tailwind CSS          | Component styling                      |
| UI Components         | shadcn/ui, Radix UI   | Reusable interface components          |
| Backend               | Python                | Application logic                      |
| AI Orchestration      | LangGraph, LangChain  | Multi-stage AI workflows               |
| Language Model        | Mistral AI            | Creative content generation            |
| Embeddings            | Mistral AI Embeddings | Semantic representation                |
| Vector Database       | ChromaDB              | Trend retrieval                        |
| Data Integration      | Apify                 | External trend datasets                |
| Multimedia Processing | Python utilities      | Audio, video, and stitching operations |
| Configuration         | python-dotenv         | Environment-based API configuration    |

---

## System Architecture

```text
                         USER
                          |
                          v
              +-----------------------+
              |     MUSE FRONTEND     |
              |   React + TypeScript  |
              |      Vite + UI        |
              +-----------+-----------+
                          |
                          v
              +-----------------------+
              |     PYTHON BACKEND    |
              |        main.py        |
              +-----------+-----------+
                          |
         +----------------+----------------+
         |                |                |
         v                v                v
 +---------------+ +---------------+ +---------------+
 |   WORKFLOW 1  | |   WORKFLOW 2  | |   WORKFLOW 3  |
 | Meme Ideation | | Media Content | |  Publishing   |
 |               | |   Generation  | |               |
 +-------+-------+ +-------+-------+ +---------------+
         |                 |
         v                 v
 +---------------+ +-------------------+
 | LangGraph     | | Multimedia Utils  |
 | Mistral AI    | | Audio Processing  |
 | ChromaDB      | | Video Processing  |
 | Apify         | | Media Stitching   |
 +---------------+ +-------------------+
```

### Meme Idea Generation Pipeline

```text
Product Information
        |
        v
Load Local Meme Trends
        |
        +------> Fetch External Trends (Apify)
        |                    |
        +--------------------+
        |
        v
Create Trend Documents
        |
        v
Generate Vector Embeddings
        |
        v
Store / Retrieve with ChromaDB
        |
        v
Build Contextual AI Prompt
        |
        v
Mistral AI Generation
        |
        v
Validate Structured JSON
        |
        v
Return Meme Advertisement Ideas
```

---

## Project Structure

```text
Hack_submission/
|
+-- backend/
|   |
|   +-- main.py
|   +-- flow1_memegen.py
|   +-- flow2_generate.py
|   +-- flow3_publish.py
|   +-- meme_trends.json
|   +-- requirements.txt
|   |
|   +-- utils/
|   |   +-- audio.py
|   |   +-- video.py
|   |   +-- stitch.py
|   |
|   +-- test_script.py
|   +-- test_assets/
|   +-- README.md
|
+-- frontend/
|   |
|   +-- src/
|   |   +-- App.tsx
|   |   +-- App.css
|   |   +-- main.tsx
|   |   +-- index.css
|   |   |
|   |   +-- components/
|   |   |   +-- layout/
|   |   |   +-- ui/
|   |   |
|   |   +-- pages/
|   |   |   +-- HomePage.tsx
|   |   |   +-- DashboardPage.tsx
|   |   |   +-- ProjectsPage.tsx
|   |   |   +-- ProjectPage.tsx
|   |   |   +-- CampaignPage.tsx
|   |   |   +-- VideoStudioPage.tsx
|   |   |   +-- AnalyticsPage.tsx
|   |   |   +-- SettingsPage.tsx
|   |   |
|   |   +-- store/
|   |   +-- types/
|   |   +-- hooks/
|   |   +-- lib/
|   |
|   +-- package.json
|   +-- package-lock.json
|   +-- vite.config.ts
|   +-- tailwind.config.js
|   +-- tsconfig.json
|
+-- .gitignore
+-- README.md
+-- flow.md
+-- LICENSE
```

Temporary uploads, local vector database files, dependencies, and environment secrets should remain excluded from version control.

---

## Installation and Setup

### Prerequisites

Before running MUSE, install:

- Python 3.12 or another version compatible with the pinned dependencies.
- Node.js and npm.
- Git.
- A Mistral AI API key.
- An Apify API token if live trend retrieval is required.
- Credentials for any additional generation or publishing integrations used by the backend.

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Mashielkhan/Hack_submission.git
cd Hack_submission
```

### Step 2 — Configure the Backend

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

The Windows-compatible dependency configuration should conditionally exclude `uvloop`, which is unsupported on native Windows.

### Step 3 — Configure Environment Variables

Create a `.env` file inside `backend/`:

```ini
MISTRAL_API_KEY=your_mistral_api_key
APIFY_API_TOKEN=your_apify_api_token
APIFY_DATASET_ID=your_dataset_id
```

The default dataset ID may already be configured in the backend implementation.

Additional variables may be required depending on the content-generation and publishing services used.

**Security:** Never commit `.env` or actual API credentials to version control. Any previously exposed keys should be revoked and regenerated.

### Step 4 — Start the Python Backend

From the `backend` directory:

```bash
python main.py
```

The server address and port depend on the configuration inside `main.py`.

### Step 5 — Start the Frontend

Open a second terminal:

```bash
cd frontend
```

Install JavaScript dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL displayed by Vite, commonly:

[http://localhost:5173](http://localhost:5173)

Ensure the frontend is configured to communicate with the correct backend address.

---

## How MUSE Works

### Step 1 — Provide Product Information

The user enters a product name and description.

For example:

**Product:** Smart Coffee Mug

**Description:** A rechargeable, temperature-controlled coffee mug designed for people who work long hours.

### Step 2 — Generate Meme Concepts

The application retrieves relevant trend context and constructs a prompt for Mistral AI.

The model generates three advertisement concepts with narration and visual instructions.

### Step 3 — Review Creative Concepts

The generated output contains structured information such as:

```json
[
  {
    "idea": "When Your Coffee Never Gives Up",
    "audio_script": "Your deadlines are getting colder, but your coffee isn't.",
    "video_prompt": "A tired office worker discovers a temperature-controlled mug during a late-night work session."
  }
]
```

This is an illustrative example of the expected output format, not a recorded model response.

### Step 4 — Generate Multimedia Content

The content-generation workflow can use the selected creative concept as input for subsequent media-processing steps.

### Step 5 — Prepare Content for Publishing

The publishing workflow provides a separate backend stage for handling generated content.

The availability of automatic publishing depends on configured platform integrations and supported API functionality.

---

## Engineering Highlights

### LangGraph Workflow Orchestration

The meme-generation backend uses a graph-based workflow to process product information, retrieve contextual data, invoke an LLM, and return structured results.

### Retrieval-Augmented Generation

MUSE uses semantic retrieval to identify relevant meme trends before generating advertisements.

This provides a practical application of RAG in a creative marketing context.

### Vector Search with ChromaDB

Text embeddings allow meme descriptions to be searched according to semantic relevance.

This enables matching product descriptions with potentially relevant advertising trends.

### Structured AI Output

The idea-generation workflow requests JSON-based responses containing predictable fields for later processing.

This makes downstream content generation easier to integrate than unrestricted natural-language output.

### Modular Backend

Separate backend modules organize idea generation, media generation, and publishing into distinct responsibilities.

### Frontend Architecture

React and TypeScript provide a component-oriented UI, while Vite supports a streamlined development workflow.

---

## Development Considerations

The project uses external AI services and local data persistence, which introduces several practical considerations.

- **API availability:** AI and trend retrieval depend on third-party service uptime.
- **Usage costs:** Embedding, generation, and media services may charge per request.
- **Trend quality:** Creative relevance depends on the content and freshness of the underlying trend dataset.
- **Output reliability:** LLM-generated JSON can occasionally be invalid or incomplete.
- **Publishing access:** External platforms may require permissions and developer approval.
- **Content review:** Generated advertisements should be reviewed before public distribution.
- **Security:** API credentials and uploaded media should be handled securely.

---

## Future Roadmap

Potential enhancements include:

- Real-time trend discovery across multiple platforms.
- Advanced AI video generation.
- Brand-aware content personalization.
- Automated subtitle generation.
- Multi-platform publishing integrations.
- Campaign performance analytics.
- Content scheduling and approval workflows.
- AI-assisted hashtag and caption generation.
- Multilingual meme generation.
- Team collaboration and campaign management.
- Cloud-based media storage.
- Production-grade error handling and job queues.

These are development opportunities, not guarantees of currently implemented features.

---

## Development and Attribution

### Repository Maintainer

**Mashiel Khan**
BS Computer Science
Software Development | AI/ML | Full-Stack Applications

GitHub: [github.com/Mashielkhan](https://github.com/Mashielkhan)

---

## License

See the repository's `LICENSE` file for the applicable terms.

---

## Project Vision

MUSE demonstrates how AI-powered workflows can bring together creative reasoning, contextual information retrieval, multimedia operations, and marketing automation in one application.

The project serves as a practical example of integrating full-stack development with modern AI tooling to address real-world digital content production challenges.

**MUSE — From Product Idea to Creative Marketing Content, Powered by AI.**
