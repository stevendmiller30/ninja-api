# GitHub Copilot Instructions

## Project folder structure
- Application code is located under `src/`.
- Tests are located under `src/<app_name>/tests/`.
- Project configuration files are located under `config/`.

## Project files
Each Django app within the project follows a consistent structure:
- `__init__.py` - Initializes the app module.
- `api.py` - Contains the API endpoint definitions and logic.
- `services/` - Contains business logic and service layer code.
- `models/` - Contains database models.
- `schema/` - Contains Pydantic models for request and response validation.
- `tests/` - Contains unit and integration tests for the application.
- `management/` - Contains Django management commands for administrative tasks.
- `migrations/` - Contains database migration files.