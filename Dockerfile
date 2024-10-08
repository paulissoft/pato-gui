FROM jetpackio/devbox:latest

# Installing your devbox project
WORKDIR /app
USER root:root
RUN mkdir -p /app && chown ${DEVBOX_USER}:${DEVBOX_USER} /app
USER ${DEVBOX_USER}:${DEVBOX_USER}
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.json devbox.lock ./
RUN devbox install
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} Makefile environment.yml pyproject.toml poetry.lock ./
RUN devbox run -- make all

CMD ["devbox", "shell"]
