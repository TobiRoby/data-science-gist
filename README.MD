Starts a vs code server in a docker container. \
You can run it on any linux machine. \
Since code server is accessed via browser you can start the container wherever you want:
- local (linux/wsl)
- remote

Starting code server
1. install [docker](https://docs.docker.com/engine/install/) & [docker-compose](https://docs.docker.com/compose/install/)
2. clone repository
3. build ide image \
    `bash
    DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose build ide
    `
4. use your ssh credentials in container by running a ssh-agent with you added key \
    `bash
    ssh-add
    `

5. provide git credentials in container: \
    ` bash
    git config --global user.name "Your Name"
    git config --global user.email "youremail@yourdomain.com"
    `

6. start code server container service `ide` \
    `bash
    DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose up ide
    ` \
    Access code server via browser: `localhost:8123`

Features
- pre-commit (black & isort, flake8, pydocstyle, mypy)
- poetry
- DS paradigns
    - test setup
    - data schema validity
