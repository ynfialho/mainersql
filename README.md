# MainerSQL

Data extraction framework for RDBMS — extract query results from PostgreSQL or SQL Server and export to CSV, JSON, or Parquet.

## Install

```bash
git clone https://github.com/ynfialho/mainersql
cd mainersql
uv sync
```

## Setup

Set the `DATABASE_URL` environment variable with your database connection string:

```bash
# PostgreSQL
export DATABASE_URL="postgresql://user:password@host:5432/dbname"

# SQL Server (MSSQL)
export DATABASE_URL="mssql+pyodbc://user:password@host:1433/dbname?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
```

## Docker (for local testing)

Start test databases with Docker Compose:

```bash
docker compose -f iac/docker-compose.yml up -d
```

This starts:
- **PostgreSQL 16** on port `5432` (user: `test`, password: `test`, db: `testdb`)
- **SQL Server 2022** on port `1433` (user: `sa`, password: `Test1234!`)

Stop containers:
```bash
docker compose -f iac/docker-compose.yml down
```

## Usage

```bash
# Display results in the terminal (default)
DATABASE_URL="postgresql://..." uv run mainersql extract --query "SELECT * FROM users"

# Export to CSV (semicolon-separated)
DATABASE_URL="postgresql://..." uv run mainersql --output csv extract --query "SELECT * FROM users"

# Export to JSON
DATABASE_URL="postgresql://..." uv run mainersql --output json --output-path ./results.json extract --query "SELECT * FROM users"

# Export to Parquet
DATABASE_URL="postgresql://..." uv run mainersql --output parquet --output-path ./results.parquet extract --query "SELECT * FROM users"
```

View available options:
```bash
uv run mainersql --help
uv run mainersql extract --help
```

## Running Tests

Unit tests (no database required):
```bash
uv run pytest tests/unit/ -v
```

Integration tests (requires Docker containers running):
```bash
docker compose -f iac/docker-compose.yml up -d
uv run pytest tests/integration/ -v -m integration
```

## Architecture

| Module | Description |
|--------|-------------|
| `cli/` | Click CLI — `extract` command + `--output` / `--output-path` flags |
| `repository/` | `BaseRepository` ABC + `SQLAlchemyRepository` (PostgreSQL, MSSQL) |
| `models/` | `ConnectionConfig` dataclass, `parse_dsn()`, `QueryResult` |
| `common/` | `write_output()` — Arrow → CSV / JSON / Parquet / rich console |
| `tests/` | Unit tests (`tests/unit/`) and integration tests (`tests/integration/`) |
| `iac/` | Docker Compose for local test databases |
