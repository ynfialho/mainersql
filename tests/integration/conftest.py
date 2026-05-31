import os
import pytest
from models.connection import parse_dsn, ConnectionConfig
from repository.sqlalchemy_repo import SQLAlchemyRepository


@pytest.fixture(scope="session")
def pg_dsn() -> str:
    return os.environ.get(
        "PG_DSN", "postgresql://test:test@localhost:5432/testdb"
    )


@pytest.fixture(scope="session")
def mssql_dsn() -> str:
    return os.environ.get(
        "MSSQL_DSN",
        "mssql+pyodbc://sa:Test1234!@localhost:1433/master"
        "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes",
    )


@pytest.fixture(scope="session")
def pg_repo(pg_dsn: str) -> SQLAlchemyRepository:
    return SQLAlchemyRepository(parse_dsn(pg_dsn))


@pytest.fixture(scope="session")
def mssql_repo(mssql_dsn: str) -> SQLAlchemyRepository:
    return SQLAlchemyRepository(parse_dsn(mssql_dsn))
