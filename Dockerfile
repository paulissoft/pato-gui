#syntax=docker/dockerfile:1.4

# Use the preceding syntax to be able to use:
# * COPY --link
# * RUN --mount=type=cache
# See also https://medium.com/datamindedbe/how-we-reduced-our-docker-build-times-by-40-afea7b7f5fe7.

FROM jetpackio/devbox:latest as build

ENV TARGET_DEVBOX=/root/.cache/devbox

# Installing your devbox project
WORKDIR /app
USER root:root
RUN --mount=type=cache,target=$TARGET_DEVBOX mkdir -p /app && chown ${DEVBOX_USER}:${DEVBOX_USER} /app
USER ${DEVBOX_USER}:${DEVBOX_USER}
COPY --link --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.json devbox.lock ./

RUN --mount=type=cache,target=$TARGET_DEVBOX devbox install

COPY --link --chown=${DEVBOX_USER}:${DEVBOX_USER} . .

# See output of make all in a devbox shell
RUN --mount=type=cache,target=$TARGET_DEVBOX \
		poetry build && \
		poetry install && \
		poetry lock && \
		poetry run pato-gui-build

FROM scratch

COPY --link --from=build /app/.venv /app/.venv

ENV PATH=/app/.venv/bin:$PATH

ENTRYPOINT ["./.venv/bin/pato-gui"]
