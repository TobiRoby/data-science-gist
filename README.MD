# Project features
This project contains many personal Data Science tips and tricks.\
Look into the [quickstart section](#quickstart-aka-developing-in-a-container) for trying them out yourself.

Features:
1. develop and test code in production environment ([code server](https://coder.com/docs/code-server/latest) in container)
2. high code reproducibility with deterministic environments (container & [poetry](https://python-poetry.org/))
3. code review automation ([pre-commit](https://pre-commit.com/), [black](https://black.readthedocs.io/en/stable/) & [isort](https://pycqa.github.io/isort/), [flake8](https://flake8.pycqa.org/en/latest/), [pydocstyle](http://www.pydocstyle.org/en/stable/) and [mypy](http://mypy-lang.org/))
4. personal Data Science paradigms
    - [data schema validity](#data-schema-validity)
    - [test setup](#test-setup)
    - utilizing interactive development possibility based on jupyter with vs code's [python](https://open-vsx.org/extension/ms-python/python) extension

# 1. Quickstart aka. developing in a container

Tested with linux and wsl2 on windows.

## Prerequisite
1. Install [docker](https://docs.docker.com/engine/install/) & [docker-compose](https://docs.docker.com/compose/install/)
2. Clone repository

## Start container
1. Build docker image (`ide` service)
    ```bash
    DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose build ide
    ```

2. Start `ide` service
    ```bash
    DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose up ide
    ```

3. Access code server via browser: `localhost:8123`\
 You are accessing vs code in the container.\
 Tip: use a chrome based browser and install the `code-server` app from that browser.\
 Thus, your vs code experience comes close of running native vs code (e.g. nearly 100% working keyboard shortcuts).

4. Optional: Rename existing `.vscode/settings.json.example` to `.vscode/settings.json` in the IDE to quickly apply suggested vscode configurations.

## Build in functionality
1. Use your host ssh credentials in the container.\
 Add your key to your hosts ssh-agent before starting the container.
    ```bash
    ssh-add
    ```

2. Provide host's git credentials to container:
    ``` bash
    git config --global user.name "Your Name"
    git config --global user.email "youremail@yourdomain.com"
    ```
    Note: If you have no git credentials on your host system this can lead to ugly mounting behavior. Remove the `.gitconfig` mount in `docker-compose.yaml` file, to remove this feature

## Developing in a container benefits and downsides:
Benefits:
- develop either on your local system or any remote machine you want. (remote development requires only port forwarding to your local system, e.g. via `ssh`)
- no `does not run on my machine` problems.
- deployed code (container) behaves the same way as when you are developing. (sharing deterministic environment)
- combining common ide features (like debugging and testing functionality) with - often essential - interactive `jupyter` development.
- full open source solution. Not closed source like vs code's [remote extensions](https://code.visualstudio.com/docs/remote/remote-overview#_remote-development-extension-pack).

Downsides:
- harder (but possible) customization when working with multiple people.
- being a little (1-2 months) behind the latest vs code releases, due to integration dependency of code server project.

# 2. High code reproducibility with deterministic environments
High code reproducibility is very important when:
- checking out and testing new feature (branches) in development
- deploying code from development into a productive environment
- debugging productive code in a safe development environment

Deterministic environments are majorly achieved by two technologies used in this project:
1. [docker](https://www.docker.com/) for deterministic virtualized images and containers
2. [poetry](https://python-poetry.org/) as a deterministic python package manager

Both technologies can be replaced via drop in replacements like [podman](https://podman.io/) for docker and [pipenv](https://pipenv.pypa.io/en/latest/) for poetry.

# 3. Code review automation
Focusing on your main project goals and achieving them is our main goal.\
One way of freeing time in code reviews is by automating and enforcing code standards.

First you need to decide what code standards you want to apply in your project.
This project contains the following tools:
- [black](https://black.readthedocs.io/en/stable/) & [isort](https://pycqa.github.io/isort/) for automated code formatting
- [flake8](https://flake8.pycqa.org/en/latest/) & [mypy](http://mypy-lang.org/) for linting and preventing common errors
- [pydocstyle](http://www.pydocstyle.org/en/stable/) for documentation

Afterwards you can automate and thus enforcing them in your project.\
With [pre-commit](https://pre-commit.com/) you can run your tool suite before every git commit making it easy for everyone to follow them.

# 4. Personal Data Science paradigms
## Data Schema Validity
The project shows how to use [pandera](https://pandera.readthedocs.io/en/stable/) for defining data schemas with automatic schema checks.\
Since the schemas are configured to be `strict` we know data schema at every major step in the data pipeline.\
This makes debugging and testing code straight forwards and easier for everyone not familiar with the project.

## Test Setup
Separating tests into the following aspects worked in multiple projects:
- unit: deterministic function tests
- integration: especially checking schema validity incl. external sources
- end2end: quick run tests for more complex data pipelines (e.g. model training and scoring)
- infrastructure: end2end test including tests for infrastructure connectivity (e.g. querying hosted API)

## VS Code extensions
tbd
