import csv
import pytest
import pyarrow as pa
from repository.sqlalchemy_repo import SQLAlchemyRepository
from common.output import write_output


def _odbc_driver_available() -> bool:
    try:
        import pyodbc
        return "ODBC Driver 17 for SQL Server" in pyodbc.drivers()
    except Exception:
        return False


@pytest.mark.integration
def test_pg_extract_select_1(pg_repo: SQLAlchemyRepository):
    table = pg_repo.execute_query("SELECT 1 AS val")
    assert isinstance(table, pa.Table)
    assert table.num_rows == 1
    assert "val" in table.schema.names


@pytest.mark.integration
@pytest.mark.skipif(
    not _odbc_driver_available(),
    reason="ODBC Driver 17 for SQL Server not installed",
)
def test_mssql_extract_select_1(mssql_repo: SQLAlchemyRepository):
    table = mssql_repo.execute_query("SELECT 1 AS val")
    assert isinstance(table, pa.Table)
    assert table.num_rows == 1
    assert "val" in table.schema.names


@pytest.mark.integration
def test_pg_extract_output_csv(pg_repo: SQLAlchemyRepository, tmp_path):
    table = pg_repo.execute_query("SELECT 1 AS id, 'test' AS name")
    path = write_output(table, "csv", str(tmp_path / "out.csv"))
    rows = list(csv.reader(open(path), delimiter=";"))
    assert rows[0] == ["id", "name"]
    assert len(rows) == 2  # header + 1 data row
