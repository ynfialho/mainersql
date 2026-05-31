from dataclasses import dataclass

import pyarrow as pa


@dataclass
class QueryResult:
    table: pa.Table
    row_count: int
    columns: list[str]
