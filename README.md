# ExplainMyRepo

This is an AI-powered tool that takes a GitHub repository as input and generates a clear, human-readable explanation of the codebase. It helps developers, students, and reviewers quickly understand unfamiliar projects without manually navigating through files.

## Overview

Understanding a new codebase can be time-consuming and difficult. RepoExplainer automates this process by analyzing the structure and contents of a repository and converting them into structured explanations that describe how the project works.

## Features

- Analyzes repository folder and file structure
- Identifies important files and modules
- Explains core logic and workflows
- Generates structured, readable documentation
- Reduces onboarding and code review time

## Use Cases

- Developers exploring open-source projects
- Students learning from real-world repositories
- Hackathon reviewers evaluating submissions
- Teams onboarding new contributors

## Project Status

Initial implementation has started. The repository now includes a FastAPI backend scaffold,
environment-based settings, baseline quality tooling, and CI checks.

## Quick Start

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies:
	- `pip install -r requirements-dev.txt`
3. Run the API locally:
	- `uvicorn app.main:app --reload`
4. Verify service health:
	- Open `http://127.0.0.1:8000/health`

## Development Commands

- `pytest` to run tests
- `ruff check .` to lint
- `ruff format .` to format
- `mypy app tests` to type-check
- `pre-commit install` to enable local hooks
