# Django-api

## AI instruction files
Files used to define rules and project context for GitHub Copilot.

* .github/.copilot-instructions.md
* .github/instructions/general.instructions.md
* .github/instructions/python.instructions.md

## Technology
* [Django](https://www.djangoproject.com/)
* [Django Ninja](https://django-ninja.rest-framework.com/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Git Hub](https://github.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [VS Code Dev Container](https://code.visualstudio.com/docs/devcontainers/containers)
* [Elasticsearch](https://www.elastic.co/)
* [LM Studio](https://lmstudio.ai/)
* [UV](https://docs.astral.sh/uv/)
* [Ruff](https://docs.astral.sh/ruff/)

## Prerequisits
* VS Code with "Dev Containers" Marketplace Extension
* git
* Docker Desktop

### Github key
```
$ ssh-keygen -t ed25519 -C "your_email@example.com" # add to github settings
$ ssh-add -l # verify key
# copy ~/.ssh/id_ed25519 to github settings/ssh keys...
$ git config --global user.email "youremail@domain.com"
$ git config --global user.name "name"
```

## Project Structure
* .devcontainer --> VS Code dev container configuration
* .vscode --> VS Code configuration
* rest_client --> collection of API calls (get, post, put, patch, delete)
* config --> Django Ninja configuration
* src --> Project code
  * <appname>/management --> custom management commands
  * <appname>/migrations --> db migrations
  * <appname>/models --> db models
  * <appname>/schemas --> Pydantic and Ninja schemas
  * <appname>/services --> Business service logic
  * <appname>/tests --> unit tests
  * <appname>/api.py --> api interface
  * <appname>/apps.py --> application configuration
  * common --> code shared among apps
* Dockerfile, docker-compose.env, and docker-compose.yml --> defines docker environment
* manage.py --> Django command line utility
* pyproject.toml, ruff.toml, uv.lock --> project dependencies and auto formatting
* pytest.int --> testing configuration

## Running Project

### optional LM Studio
* Used to run AI models locally, bypassing Copilot
* Download and install LM Studio
* Download desired models
* Run LM Studio.  Default address is http://127.0.0.1:1234
* "Continue" VS Code plugin is automatically loaded in VS Code (devcontainer.json)
* Open VS Code "CHAT"
* In top menu next to "CHAT" select "..." and select "Continue".  You are now chatting with LM Studio


### Start Application
* Click on "Run and Debug" (ctrl-shift-d) on left side bar
  * Select drop down and select "Django-Server" or "Django-Manage.py"
    * "Django-Server" will run the project
    * "Django-Manage.py" will run manage.py with a drop down to select process to run
  * Click on the Play button

### Unit Tests
* VS Code
  * Click on Beaker (Testing) icon
    * select project, folder, or file and run, debug, or run with coverage
  * run or debug tests within test file
* Unix Terminal
  * run ut, utf, and/or utr aliases

### DB Access (I use DBeaver)
* Host: localhost
* Port: 5435
* Database: ninja-api
* Username: postgres
* Password: <obtain for docker-compose.env>
* Driver name: PostgresSQL

### Elasticsearch Kibana
* used to Visualize, explore, and manage data
* http://localhost:5601