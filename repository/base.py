from abc import ABC, abstractmethod
import pyarrow as pa


class BaseRepository(ABC):
    """Contract for all repository implementations.
    
    Implementors must provide execute_query() which runs a SQL query
    and returns results as an Apache Arrow Table.
    """

    @abstractmethod
    def execute_query(self, query: str) -> pa.Table:
        """Execute SQL query and return results as Arrow Table."""
        ...
