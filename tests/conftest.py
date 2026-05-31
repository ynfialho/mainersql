import pytest
import pyarrow as pa
from models.connection import ConnectionConfig


@pytest.fixture
def sample_table() -> pa.Table:
    return pa.table({"id": [1, 2, 3], "name": ["alice", "bob", "charlie"]})


@pytest.fixture
def mock_connection_config() -> ConnectionConfig:
    return ConnectionConfig(
        dsn="postgresql://user:pass@localhost/testdb",
        dialect="postgresql",
    )
