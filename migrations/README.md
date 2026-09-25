# Database Migrations (`migrations/`)

This directory contains the Alembic configuration and migration scripts.

Alembic tracks changes to the SQLAlchemy models defined in the application's infrastructure layer and applies them to the PostgreSQL database.

## Usage Commands

- Create a new migration: `uv run alembic revision --autogenerate -m "description"`
- Apply migrations: `uv run alembic upgrade head`
- Revert the last migration: `uv run alembic downgrade -1`
