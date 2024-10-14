ARG VERSION_DEVBOX=0.13.4
ARG VERSION_ALPINE=3.20.3

ARG UID=1000
ARG GID=1000

# ---
# Stage 1 (base): install devbox and its packages
# ---
FROM jetpackio/devbox:${VERSION_DEVBOX} as base

# Installing your devbox project
WORKDIR /app
USER root:root
RUN mkdir -p /app && chown ${DEVBOX_USER}:${DEVBOX_USER} /app
USER ${DEVBOX_USER}:${DEVBOX_USER}
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.json devbox.lock ./
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} pyproject-minimal.toml ./pyproject.toml
RUN touch README.md CHANGELOG.md
RUN devbox install
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} environment.yml pyproject.toml poetry.lock ./
RUN devbox run -- echo "Installed Packages."

COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} . .
RUN devbox run -- poetry pato-gui-build

CMD ["devbox", "run", "--", "./dist/PatoGui/PatoGui"]
