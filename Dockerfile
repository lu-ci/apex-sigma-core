# |-------<[ Build ]>-------|

FROM python:3.6-slim AS build

RUN mkdir -p /build
WORKDIR /build

COPY requirements.txt ./
RUN echo "deb [check-valid-until=no] http://cdn-fastly.deb.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list \
 && echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list \
 && sed -i '/deb http:\/\/\(deb\|httpredir\).debian.org\/debian jessie.* main/d' /etc/apt/sources.list \
 && apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
 && pip install --no-cache-dir virtualenv \
 && virtualenv .venv \
 && . .venv/bin/activate \
 && pip install --no-cache-dir -r requirements.txt \
 && virtualenv --relocatable .venv \
 && sed -i -E 's|^(VIRTUAL_ENV="/)build(/.venv")$|\1app\2|' .venv/bin/activate \
 && rm -rf /var/lib/apt/lists/*


# |-------<[ App ]>-------|

FROM python:3.6-slim AS apex-sigma

LABEL maintainer="dev.patrick.auernig@gmail.com"

RUN echo "deb [check-valid-until=no] http://cdn-fastly.deb.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list \
 && echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list \
 && sed -i '/deb http:\/\/\(deb\|httpredir\).debian.org\/debian jessie.* main/d' /etc/apt/sources.list \
 && apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y \
    libxml2 \
    ffmpeg \
    bash \
 && rm -rf /var/lib/apt/lists/*

ARG user_uid=1000
ARG user_gid=1000
RUN addgroup --system --gid "$user_gid" app \
 && adduser --system --ingroup app --uid "$user_uid" app

RUN mkdir -p /app && chown app:app /app
WORKDIR /app
USER app

COPY --chown=app:app --from=build /build/.venv ./.venv
COPY --chown=app:app ./ ./

ENTRYPOINT ["/bin/bash"]
CMD ["./run.sh"]