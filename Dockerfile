# BASE
FROM python:3.9-slim-bullseye as base

ENV POETRY_HOME=/home/appuser
ENV PATH="${PATH}:${POETRY_HOME}/bin"
ENV POETRY_INSTALLER_MAX_WORKERS=10
ENV PYTHONPATH=/home/appuser/app
ENV TZ=Europe/Berlin

# set timezone to berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime &&\
    echo $TZ > /etc/timezone &&\
    apt-get update &&\
    apt-get upgrade -y --autoremove &&\
    apt-get install -y tzdata &&\
    dpkg-reconfigure --frontend noninteractive tzdata &&\
    apt-get clean

# create app folder & add to pythonpath for direct python shell execution
ARG USER_ID=1000
ARG GROUP_ID=1000

WORKDIR /home/appuser/app
RUN groupadd -g ${GROUP_ID} appuser &&\
    useradd -l -s /bin/bash -u ${USER_ID} -g appuser appuser &&\
    mkdir -p /home/appuser/.cache/pre-commit &&\
    chown ${USER_ID}:${GROUP_ID} -R /home/appuser &&\
    install -d -m 0755 -o appuser -g appuser /home/appuser

# install & source poetry
RUN apt-get update &&\
    apt-get install -y curl &&\
    apt-get clean
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.3.1

FROM base as dev
# install git
RUN apt-get update &&\
    apt-get install -y git bash-completion &&\
    apt-get clean

USER appuser
# git completion
RUN echo 'source /usr/share/bash-completion/completions/git' >> ~/.bashrc

# pyproject.toml and optional lock-file
COPY pyproject.toml poetry.lock* ./
RUN poetry install && \
    rm -rf ~/.cache/pypoetry/{cache,artifacts} && \
    rm -rf pyproject.toml poetry.lock
