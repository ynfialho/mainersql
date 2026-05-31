import csv
import json
from datetime import datetime
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from rich.console import Console
from rich.table import Table


def write_output(
    table: pa.Table,
    format: str,
    output_path: str | None = None,
) -> str | None:
    """Serialize Arrow Table to the requested format.

    Args:
        table: Apache Arrow Table with query results.
        format: One of 'console', 'csv', 'json', 'parquet'.
        output_path: File path to write. If None, auto-generated in CWD.

    Returns:
        Path string where file was written, or None for console output.
    """
    if format == "console":
        _render_rich_table(table)
        return None

    path = _resolve_output_path(format, output_path)

    if format == "csv":
        _write_csv(table, path)
    elif format == "json":
        _write_json(table, path)
    elif format == "parquet":
        pq.write_table(table, path)
    else:
        raise ValueError(f"Unsupported format: {format!r}")

    return path


def _resolve_output_path(format: str, output_path: str | None) -> str:
    if output_path:
        return output_path
    ext = {"csv": "csv", "json": "json", "parquet": "parquet"}[format]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(Path.cwd() / f"output_{timestamp}.{ext}")


def _render_rich_table(table: pa.Table) -> None:
    rich_table = Table()
    for col in table.schema.names:
        rich_table.add_column(col)
    rows_dict = table.slice(0, 1000).to_pydict()
    num_rows = min(table.num_rows, 1000)
    for i in range(num_rows):
        rich_table.add_row(*[str(rows_dict[col][i]) for col in table.schema.names])
    Console().print(rich_table)


def _write_csv(table: pa.Table, path: str) -> None:
    rows_dict = table.to_pydict()
    columns = table.schema.names
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(columns)
        for i in range(table.num_rows):
            writer.writerow([rows_dict[col][i] for col in columns])


def _write_json(table: pa.Table, path: str) -> None:
    rows = [
        {col: table.column(col)[i].as_py() for col in table.schema.names}
        for i in range(table.num_rows)
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, default=str)
