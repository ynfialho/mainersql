import inspect
import pytest
import pyarrow as pa
from unittest.mock import MagicMock, patch
from repository.base import BaseRepository
from repository.sqlalchemy_repo import SQLAlchemyRepository
from models.connection import ConnectionConfig


def test_base_repository_is_abstract():
    assert inspect.isabstract(BaseRepository)
    with pytest.raises(TypeError):
        BaseRepository()


def test_sqlalchemy_repo_execute(mock_connection_config):
    mock_row = MagicMock()
    mock_row.__getitem__ = lambda self, i: [42, "test"][i]

    mock_result = MagicMock()
    mock_result.keys.return_value = ["id", "name"]
    mock_result.fetchall.return_value = [mock_row]

    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_result
    mock_conn.__enter__ = lambda self: self
    mock_conn.__exit__ = MagicMock(return_value=False)

    mock_engine = MagicMock()
    mock_engine.connect.return_value = mock_conn

    with patch("repository.sqlalchemy_repo.create_engine", return_value=mock_engine):
        repo = SQLAlchemyRepository(mock_connection_config)
        table = repo.execute_query("SELECT id, name FROM test")

    assert isinstance(table, pa.Table)
    assert "id" in table.schema.names
    assert "name" in table.schema.names
