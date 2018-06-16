# |-------<[ Build ]>-------|

FROM python:3.6-alpine AS build

RUN mkdir -p /build
WORKDIR /build

COPY requirements.txt ./
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    libffi-dev \
    openssl-dev \
    libxml2-dev \
    libxslt-dev \
    jpeg-dev \
    libpng-dev \
    libwebp-dev \
    freetype-dev \
    ffmpeg-dev \
    linux-headers \
 && pip install --no-cache-dir virtualenv \
 && virtualenv .venv \
 && source .venv/bin/activate \
 && pip install --no-cache-dir -r requirements.txt \
 && virtualenv --relocatable .venv \
 && sed -i -E 's|^(VIRTUAL_ENV="/)build(/.venv")$|\1app\2|' .venv/bin/activate \
 && apk del .build-deps


# |-------<[ App ]>-------|

FROM python:3.6-alpine AS apex-sigma

LABEL maintainer="dev.patrick.auernig@gmail.com"

RUN apk add --no-cache \
    openssl \
    libxml2 \
    libxslt \
    jpeg \
    libpng \
    libwebp \
    freetype \
    ffmpeg

ARG user_uid=1000
ARG user_gid=1000
RUN addgroup -S -g "$user_gid" app && adduser -S -G app -u "$user_uid" app

RUN mkdir -p /app && chown app:app /app
WORKDIR /app
USER app

COPY --chown=app:app --from=build /build/.venv ./.venv
COPY --chown=app:app ./ ./

ENTRYPOINT ["/bin/sh"]
CMD ["./run.sh"]
