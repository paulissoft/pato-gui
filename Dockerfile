FROM jetpackio/devbox:latest

# Installing your devbox project
WORKDIR /app
USER root:root
RUN mkdir -p /app && chown ${DEVBOX_USER}:${DEVBOX_USER} /app
USER ${DEVBOX_USER}:${DEVBOX_USER}

ENV DEVBOX_CACHE_DIR=/tmp/devbox_cache

RUN --mount=type=cache,target=$DEVBOX_CACHE_DIR devbox init && devbox add python poetry mamba

#COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.json devbox.json
#COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.lock devbox.lock

RUN DEVBOX_DEBUG=1 devbox update && devbox install

COPY environment.yml pyproject.toml poetry.lock ./
#RUN touch README.md && mamba env create --name pato-gui --file environment.yml
#
#ENV POETRY_NO_INTERACTION=1 \
#    POETRY_VIRTUALENVS_IN_PROJECT=0 \
#    POETRY_VIRTUALENVS_CREATE=0 \
#    POETRY_CACHE_DIR=/tmp/poetry_cache
#
#RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root
#
COPY src ./src
#
#RUN conda activate pato-gui && poetry run pato-gui-build

CMD ["devbox", "shell"]
