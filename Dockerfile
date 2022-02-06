# BASE
FROM python:3.9-slim-bullseye as base

# set timezone to berlin
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get install -y tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata

# install & source poetry
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.1.12
ENV PATH="${PATH}:/root/.local/bin"

# create app folder & add to pythonpath for direct python shell execution
WORKDIR /home/root/app
ENV PYTHONPATH=/home/root/app

FROM base as ide
# install git
RUN apt-get install -y git bash-completion \
    && apt-get clean \
    && echo 'source /usr/share/bash-completion/completions/git' >> ~/.bashrc

# TODO newer version (problems with not finding poetry in ENV)
# install code-server
RUN curl -fOL https://github.com/cdr/code-server/releases/download/v3.12.0/code-server_3.12.0_amd64.deb; \
    dpkg -i code-server_3.12.0_amd64.deb \
    && rm code-server_3.12.0_amd64.deb

# extensions to code-server
RUN SERVICE_URL="https://open-vsx.org/vscode/gallery" \
    ITEM_URL="https://open-vsx.org/vscode/item" \
    code-server --install-extension ms-python.python \
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

# TODO remove
RUN git config --global user.email "tobias.rippel@gmx.de"
RUN git config --global user.name "Tobias Rippel"

FROM base as app
# pyproject.toml and required lock-file
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev \
    && rm -rf ~/.cache/pypoetry/{cache,artifacts}
COPY . .

# start app
CMD poetry run python run_app.py
