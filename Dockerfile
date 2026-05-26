FROM python:3.14-slim as base
 
RUN addgroup --system appuser \
    && adduser --system --ingroup appuser --home /home/appuser appuser \
    && mkdir -p /home/appuser \
    && chown -R appuser:appuser /home/appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install --no-install-recommends -y curl build-essential libpq-dev  postgresql-client && \
    rm -rf /var/lib/apt/lists/*
 
COPY  --chown=appuser:appuser pyproject.toml uv.lock /app/

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/home/appuser/venv"
ENV PATH="/home/appuser/venv/bin:$PATH"

RUN uv venv /home/appuser/venv && \
    uv sync --no-install-project

COPY --chown=appuser:appuser . /app

# add deployed specific info
FROM base as deploy-env

USER appuser

# instructions for local dev-container-env
FROM base as dev-container-env

RUN apt-get update && \
    apt-get install --no-install-recommends -y bash-completion openssh-client git sudo vim && \
    rm -rf /var/lib/apt/lists/*

COPY --chown=appuser:appuser .devcontainer/db_migrate.sh /usr/local/bin/db_migrate
RUN sed -i 's/\r$//g' /usr/local/bin/db_migrate && \
    chmod +x /usr/local/bin/db_migrate
    
USER appuser

# create alias 
RUN echo 'alias ut="coverage run -m pytest"' >> ~/.bashrc
RUN echo 'alias utf="coverage run -m pytest --lf"' >> ~/.bashrc
RUN echo 'alias utr="coverage report"' >> ~/.bashrc

