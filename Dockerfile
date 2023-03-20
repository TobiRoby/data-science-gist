# BASE
FROM python:3.10-slim-bullseye as base

# set timezone to berlin
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y --autoremove \
    && apt-get install -y tzdata \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && apt-get clean

# install & source poetry
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0b1
ENV PATH="${PATH}:/root/.local/bin"
ENV POETRY_VIRTUALENVS_CREATE=False
ENV POETRY_INSTALLER_MAX_WORKER=10

# create app folder & add to pythonpath for direct python shell execution
WORKDIR /home/root/app
ENV PYTHONPATH=/home/root/app

FROM base as ide
# install git
RUN apt-get update \
    && apt-get install -y git bash-completion \
    && apt-get clean \
    && echo 'source /usr/share/bash-completion/completions/git' >> ~/.bashrc

# install code-server
RUN curl -fOL https://github.com/cdr/code-server/releases/download/v4.11.0/code-server_4.11.0_amd64.deb; \
    dpkg -i code-server_4.11.0_amd64.deb \
    && rm code-server_4.11.0_amd64.deb

# extensions to code-server
RUN code-server --install-extension ms-python.python \
    code-server --install-extension ms-pyright.pyright \
    code-server --install-extension mhutchie.git-graph \
    code-server --install-extension njpwerner.autodocstring \
    code-server --install-extension streetsidesoftware.code-spell-checker \
    code-server --install-extension njzy.stats-bar

# pyproject.toml and optional lock-file
COPY pyproject.toml poetry.lock* ./
RUN poetry install \
    && rm -rf ~/.cache/pypoetry/{cache,artifacts} \
    && rm pyproject.toml poetry.lock

# temporary fix for not correct path in vscode terminals (https://github.com/coder/code-server/issues/4699)
RUN echo "export PATH=$PATH" >> /root/.bashrc

FROM base as app
# pyproject.toml and required lock-file
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev \
    && rm -rf ~/.cache/pypoetry/{cache,artifacts}
COPY . .

# start app
CMD poetry run python project/main.py
