FROM python:3.6-slim

LABEL maintainer="dev.patrick.auernig@gmail.com"

# Build dependencies
RUN apt-get update -y \
 && apt-get install -y --no-install-recommends \
    build-essential \
    libav-tools \
 && rm -rf /var/lib/apt/lists/*

# User setup
ARG app_user=app
ARG app_user_uid=1000
ARG app_user_gid=1000

RUN groupadd -g "$app_user_gid" "$app_user" \
 && useradd -m -g "$app_user_gid" -u "$app_user_uid" -s /bin/bash "$app_user"

# Project setup
ENV APP_ROOT=/app
RUN mkdir -p "$APP_ROOT"
WORKDIR $APP_ROOT

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chown -R "$app_user_uid:$app_user_gid" "$APP_ROOT"

USER $app_user
ENTRYPOINT ["python3.6"]
CMD ["./run.py"]
