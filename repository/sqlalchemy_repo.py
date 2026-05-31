import pyarrow as pa
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from models.connection import ConnectionConfig
from repository.base import BaseRepository


class SQLAlchemyRepository(BaseRepository):
    def __init__(self, config: ConnectionConfig) -> None:
        self._engine = create_engine(config.dsn)

    def execute_query(self, query: str) -> pa.Table:
        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(query))
                columns = list(result.keys())
                rows = result.fetchall()
                data = {col: [row[i] for row in rows] for i, col in enumerate(columns)}
                return pa.table(data)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Query execution failed: {e}") from e
