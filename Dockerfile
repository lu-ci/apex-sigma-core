FROM python:3.9-slim

LABEL maintainer="dev.patrick.auernig@gmail.com"

ARG user_uid=1000
ARG user_gid=1000
RUN addgroup --system --gid "$user_gid" app \
 && adduser --system --ingroup app --uid "$user_uid" app

RUN mkdir -p /app && chown app:app /app

COPY --chown=app:app ./ /app

RUN echo "deb [check-valid-until=no] http://cdn-fastly.deb.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list \
 && echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list \
 && sed -i '/deb http:\/\/\(deb\|httpredir\).debian.org\/debian jessie.* main/d' /etc/apt/sources.list \
 && apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    git \
    ffmpeg \
    bash \
 && python -m pip install -U pip
 && pip install --no-cache-dir virtualenv \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
USER app

RUN virtualenv .venv \
 && . .venv/bin/activate \
 && python -m pip install -U pip \
 && pip install --no-cache-dir -r requirements.txt \
 && sed -i -E 's|^(VIRTUAL_ENV="/)build(/.venv")$|\1app\2|' .venv/bin/activate

ENTRYPOINT ["/bin/bash"]
CMD ["./run.sh"]
