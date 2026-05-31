import csv
import json
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from common.output import write_output


@pytest.fixture
def table():
    return pa.table({"id": [1, 2], "name": ["alice", "bob"]})


def test_csv_output_semicolon(table, tmp_path):
    path = write_output(table, "csv", str(tmp_path / "out.csv"))
    rows = list(csv.reader(open(path), delimiter=";"))
    assert rows[0] == ["id", "name"]
    assert len(rows) == 3  # header + 2 data rows


def test_json_output_valid(table, tmp_path):
    path = write_output(table, "json", str(tmp_path / "out.json"))
    data = json.load(open(path))
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "alice"


def test_parquet_output_readable(table, tmp_path):
    path = write_output(table, "parquet", str(tmp_path / "out.parquet"))
    t2 = pq.read_table(path)
    assert t2.num_rows == 2
    assert t2.schema.names == ["id", "name"]
