# Tasks API

## How to run

```bash
uv sync
uv run fastapi dev main.py
```

## How to test

```bash
uv run pytest
```

## Run the database

Start PostgreSQL:

```bash
docker compose up -d
```

Apply database migrations:

```bash
uv run alembic upgrade head
```