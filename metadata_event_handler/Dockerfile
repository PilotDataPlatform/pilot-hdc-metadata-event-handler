FROM docker-registry.ebrains.eu/hdc-services-image/base-image:python-3.10.14-v1  AS metadata_event_handler-image

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml .
COPY ./metadata_event_handler ./metadata_event_handler
COPY ./commons ./commons
COPY ./kafka_schemas ./metadata_event_handler/kafka_schemas


RUN poetry install --no-dev --no-root --no-interaction

RUN chown -R app:app /app
USER app

ENTRYPOINT ["python3", "-m", "metadata_event_handler"]
