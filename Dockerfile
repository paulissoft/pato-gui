# Access denied while getting this image from ghcr.
#
# FROM ghcr.io/prefix-dev/pixi:0.28.2 AS install

ARG PIXI_VERSION=0.31.0
ARG BASE_IMAGE=debian:bookworm-slim

FROM --platform=$TARGETPLATFORM ubuntu:24.04 AS pixi_builder
# need to specify the ARG again to make it available in this stage
ARG PIXI_VERSION
RUN apt-get update && apt-get install -y curl
# download the musl build since the gnu build is not available on aarch64
RUN curl -Ls \
    "https://github.com/prefix-dev/pixi/releases/download/v${PIXI_VERSION}/pixi-$(uname -m)-unknown-linux-musl" \
    -o /pixi && chmod +x /pixi
RUN /pixi --version

FROM --platform=$TARGETPLATFORM $BASE_IMAGE as builder
COPY --from=pixi_builder --chown=root:root --chmod=0555 /pixi /usr/local/bin/pixi

# Create a dummy blank project
WORKDIR /app/src
RUN touch __init__.py

# Install dependencies
WORKDIR /app
RUN touch README.md
COPY pixi.toml pixi.lock ./
RUN --mount=type=cache,target=/root/.cache/rattler/cache,sharing=private pixi install

# Build all: make all -n
COPY . .
RUN pixi exec poetry build
RUN apt-get update && \
    apt-get -y install gcc && \
		type gcc
RUN pixi exec poetry install
RUN pixi exec poetry lock
RUN pixi exec poetry check
RUN pixi exec poetry run pytest
RUN pixi exec poetry run pato-gui-build

ENV ENV=default

# Create an "entrypoint.sh" script which activates the pixi environment
RUN printf '#!/bin/sh\n%s\nexec "$@"' "$(pixi shell-hook -e ${ENV})" > /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Final minimal production image
FROM scratch AS production

# only copy the production environment into prod container
COPY --from=builder /app/.pixi/envs/${ENV} /app/.pixi/envs/${ENV}
COPY --from=builder /entrypoint.sh /entrypoint.sh
COPY --from=builder /app/dist/PatoGui/PatoGui /app/bin/PatoGui
WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]  # uses the pixi environment
CMD ["/app/bin/PatoGui"]
