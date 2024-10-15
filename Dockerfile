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
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} pyproject.toml poetry.lock ./
RUN devbox run -- echo "Installed Packages."

COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} . .
RUN devbox run -- make all

ENV PATH=/home/${DEVBOX_USER}/micromamba/envs/pato-gui:${PATH}

USER root:root
WORKDIR /tmp
ENV HICOLOR_ICON_THEME=hicolor-icon-theme-0.18
RUN curl -O https://icon-theme.freedesktop.org/releases/${HICOLOR_ICON_THEME}.tar.xz && \
    tar -xvf ${HICOLOR_ICON_THEME}.tar.xz && \
    cd ${HICOLOR_ICON_THEME} && \
    meson setup build --prefix /usr && \
    meson install -C build
USER ${DEVBOX_USER}:${DEVBOX_USER}

# micromamba run -n pato-gui poetry run pato-gui
# CMD ["devbox", "run", "--", "micromamba", "run", "-n", "pato-gui", "poetry", "run", "pato-gui"]
CMD ["devbox", "shell"]
