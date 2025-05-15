FROM ghcr.io/astral-sh/uv:debian

ARG user_uid=1000
ARG user_gid=1000
RUN addgroup --system --gid "$user_gid" app \
 && adduser --system --ingroup app --uid "$user_uid" app

RUN apt-get update \
 && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    git \
    ffmpeg \
    bash \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app && chown app:app /app
COPY --chown=app:app ./ /app
WORKDIR /app
USER app

ENV UV_CACHE_DIR=/app/.uv-cache
ENV UV_FROZEN=1

RUN uv venv
RUN uv pip install -Ur requirements.txt

ENTRYPOINT ["/bin/bash"]
CMD ["./run.sh"]
