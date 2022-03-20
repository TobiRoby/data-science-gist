# Project features
This project contains many personal Data Science tips and tricks and a quickstart for you to try them out yourself:

- high code reproducibility with deterministic environments (container & [poetry](https://python-poetry.org/))
- develop and test in production environment ([code server](https://coder.com/docs/code-server/latest) meets container)
- high degree of code review automatization with [pre-commit](https://pre-commit.com/), [black](https://black.readthedocs.io/en/stable/) & [isort](https://pycqa.github.io/isort/), [flake8](https://flake8.pycqa.org/en/latest/), [pydocstyle](http://www.pydocstyle.org/en/stable/) and [mypy](http://mypy-lang.org/)
- some personal Data Science paradigms
    - utilizing interactive development possibility based on jupyter with vs code's [python](https://open-vsx.org/extension/ms-python/python) extension
    - code structuring (tbd)
    - test setup (tbd)
    - data schema validity (tbd)
    - ...

# Quickstart aka. start developing in a container

Supported under linux and wsl2 on windows.

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
 Note: use a chrome based browser and install the `code-server` app -> experience comes close of running native vs code (e.g. nearly 100% working keyboard shortcuts)

## Build in functionality
1. Use your host ssh credentials in the container. \
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

Solution benefits:
- develop either on your local system or any remote machine you want. (remote development requires only port forwarding to your local system, e.g. via `ssh`)
- no `does not run on my machine` problems
- deployed code (container) behaves the same way as when you developed it (sharing deterministic environment)
- combining common ide features (like debugging and testing functionality) with - often essential - interactive `jupyter` development
- full open source solution and not closed source like vs code's [remote extensions](https://code.visualstudio.com/docs/remote/remote-overview#_remote-development-extension-pack).

Solution downsides:
- harder (but possible) customization when working with multiple people
- being a little (1-2 months) behind the latest vs code releases, due to integration dependency of code server project.

# Reproducibility with containers (docker) and poetry
tbd
# Code review automatization
tbd
# Personal Data Science paradigms
tbd
# VS Code extensions
tbd
