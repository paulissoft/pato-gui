#syntax=docker/dockerfile:1.4

# Use the preceding syntax to be able to use:
# * COPY --link
# * RUN --mount=type=cache
# See also https://medium.com/datamindedbe/how-we-reduced-our-docker-build-times-by-40-afea7b7f5fe7.

FROM jetpackio/devbox:latest as build



# Installing your devbox project
WORKDIR /app
USER root:root
RUN mkdir -p /app && chown ${DEVBOX_USER}:${DEVBOX_USER} /app
USER ${DEVBOX_USER}:${DEVBOX_USER}
COPY --link --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.json devbox.lock ./

ENV GIT_CACHE=/tmp/git_cache/
# RUN --mount=type=cache,target=${GIT_CACHE} DEVBOX_DEBUG=1 devbox run -- echo "Installed Packages."

COPY --link --chown=${DEVBOX_USER}:${DEVBOX_USER} . .

USER root:root
RUN find / -print
USER ${DEVBOX_USER}:${DEVBOX_USER}

# See output of make all in a devbox shell
# RUN . /app/.venv/bin/activate && type -p poetry && poetry build && poetry install && poetry lock && poetry run pato-gui-build

# FROM scratch

# COPY --link --from=build /app /app
# RUN find /app -print

ENV PATH=/app/.venv/bin:$PATH

ENTRYPOINT ["/bin/sh"]
