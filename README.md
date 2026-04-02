# ExplainMyRepo

ExplainMyRepo is an AI-powered repository understanding tool.
It accepts a GitHub repository URL and returns a structured explanation with:

- Overview
- Core modules summary
- Likely workflow
- Grounding citations
- Markdown and JSON output formats

The project includes a FastAPI backend and a minimal Streamlit frontend.

## Current Capabilities

- Repository URL validation for GitHub links
- Analysis orchestration pipeline with structured output
- Retry, timeout, and error-wrapped LLM calls
- Streaming analysis endpoint (SSE)
- Export endpoint (markdown/json)
- In-memory TTL cache for repeated analysis requests
- Basic observability metrics endpoint
- Streamlit UI for human-friendly input/output

## Architecture (High Level)

1. Client submits a repository URL.
2. API validates input and calls the analysis orchestrator.
3. Orchestrator builds context and requests sectioned explanation text from configured LLM provider.
4. Result is formatted as markdown + JSON with citations.
5. Cached result is reused when available.

## Tech Stack

- Python 3.11
- FastAPI
- httpx
- pydantic-settings
- Streamlit
- Ruff, mypy, pytest, pre-commit

## Quick Start

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies:
	- `pip install -r requirements-dev.txt`
3. Start API:
	- `uvicorn app.main:app --reload`
4. Verify API:
	- `http://127.0.0.1:8000/health`
5. Start Streamlit UI (new terminal):
	- `streamlit run streamlit_app.py`
6. Open UI:
	- `http://localhost:8501`

## LLM Provider Configuration

Create `.env` from `.env.example` and set values:

- `EXPLAIN_MY_REPO_LLM_PROVIDER=template` or `gemini`
- `EXPLAIN_MY_REPO_GEMINI_API_KEY=<your_key>`
- `EXPLAIN_MY_REPO_GEMINI_MODEL=gemini-2.5-flash`

Notes:

- `template` mode is useful for local/offline development.
- `gemini` mode produces real model output.

## API Endpoints

- `GET /health`
- `POST /analyze`
- `POST /analyze/form`
- `POST /analyze/stream`
- `POST /analyze/export`
- `GET /metrics`
- `GET /` (minimal HTML page)

OpenAPI docs:

- `http://127.0.0.1:8000/docs`

### Example Analyze Request

```json
{
  "repository_url": "https://github.com/psf/requests"
}
```

### Example Export Request

```json
{
  "repository_url": "https://github.com/psf/requests",
  "format": "markdown"
}
```

## Development Commands

- `ruff check .`
- `ruff format .`
- `mypy app tests`
- `pytest -q`
- `pre-commit install`

## Project Status

The repository is in active implementation with a working backend, test suite, provider abstraction, caching, observability, and Streamlit UI.
