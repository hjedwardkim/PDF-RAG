FROM python:3.9-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev
RUN pip install --no-cache-dir poetry=="$POETRY_VERSION"
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
EXPOSE 8000
COPY . /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
