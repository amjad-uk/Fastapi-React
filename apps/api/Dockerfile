FROM python:3.11-slim AS base
ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app
WORKDIR /app
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml ./
RUN pip install --no-cache-dir pip setuptools wheel && pip install --no-cache-dir -e .
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY pytest.ini /app/pytest.ini
COPY tests /app/tests
COPY app/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
