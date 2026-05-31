import pytest
from models.connection import ConnectionConfig, parse_dsn


def test_parse_dsn_postgresql():
    config = parse_dsn("postgresql://user:pass@localhost/db")
    assert config.dialect == "postgresql"
    assert config.dsn == "postgresql://user:pass@localhost/db"


def test_parse_dsn_mssql():
    config = parse_dsn("mssql+pyodbc://sa:pass@localhost/master")
    assert config.dialect == "mssql"


def test_parse_dsn_invalid():
    with pytest.raises(ValueError, match="Unsupported DSN dialect"):
        parse_dsn("mysql://user:pass@localhost/db")
