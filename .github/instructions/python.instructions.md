---
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py'
---

# Python Project Instructions

## Project Context
- **Framework:** Django Ninja for backend API.
- **Database:** PostgreSQL.
- **Environment:** Use Python 3.14+ features exclusively.

## Coding Standards
- **Style Guide:** Strictly follow [PEP 8](https://python.org) for all code generation.
- **Naming:** 
  - Use `snake_case` for all functions and variables.
  - Use `PascalCase` for classes.
- **Formatting:** use ruff formatting with instructions in `ruff.toml` 
- **Documentation:** Include function and class docstrings immediately after the definition using the Google style format.

## Architecture & Logic
- **Error Handling:** Never fail silently. Raise HTTP 4xx or 5xx errors with descriptive messages for the frontend.
- **Typing:** Enforce strict type hinting for all function signatures and variable declarations.
- **Interactivity:** For CLI tools, use the `typer` library for command-line interface generation.

## Testing Requirements
- **Framework:** Use `django.test.TestCase` for all unit and integration tests.
- **Coverage:** Aim for 100% coverage on new features; always generate a test file alongside new logic.
