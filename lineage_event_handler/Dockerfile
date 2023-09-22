FROM python:3.10.4-buster

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml ./
COPY ./lineage_event_handler ./lineage_event_handler
COPY ./commons ./commons
COPY ./kafka_schemas ./lineage_event_handler/kafka_schemas

RUN poetry install --no-dev --no-root --no-interaction

ENTRYPOINT ["python3", "-m", "lineage_event_handler"]
