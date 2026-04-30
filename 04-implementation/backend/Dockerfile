FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Wait for Postgres to accept connections, then migrate and start
CMD ["sh", "-c", "until pg_isready -h ${POSTGRES_HOST:-postgres} -U ${POSTGRES_USER:-iris}; do echo 'waiting for postgres...'; sleep 2; done && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
