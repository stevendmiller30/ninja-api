# base project
Starting point for a Containerized Django Ninja project.  Inital db is base-db which should be renamed.

## AI instruction files
Files used to define rules and project context for GitHub Copilot.

* .github/.copilot-instructions.md
* .github/instructions/general.instructions.md
* .github/instructions/python.instructions.md

## Technology
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Git Hub](https://github.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [VS Code Dev Container](https://code.visualstudio.com/docs/devcontainers/containers)
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

### Unit Testsases

### DB Access (I use DBeaver)
* Host: localhost
* Port: 5435
* Database: base-db
* Username: postgres
* Password: <obtain for docker-compose.env>
* Driver name: PostgresSQL
