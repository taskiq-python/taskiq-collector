FROM node:lts-alpine3.16 as front

COPY frontend/package.json frontend/yarn.lock /app/
WORKDIR /app
RUN yarn install

COPY frontend/ .
RUN yarn generate

FROM python:3.9.13-alpine3.16

RUN apk add --no-cache postgresql-libs mariadb-connector-c-dev libstdc++ \
    && apk add --update --no-cache --virtual .build-deps \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev \
    build-base \
    postgresql-dev \
    python3-dev \
    mariadb-dev \
    # Installing poetry
    && pip install --no-cache-dir poetry==1.1.13 \
    # Configuring poetry
    && poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install -E mysql -E pg

# Removing gcc
RUN apk --purge del .build-deps

# Copying actuall application
COPY . /app/src/

COPY --from=front /app/dist /app/src/taskiq_collector/static/front
RUN poetry install -E mysql -E pg --no-dev

CMD ["/usr/local/bin/python", "-m", "taskiq_collector"]
