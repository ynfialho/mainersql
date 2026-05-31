import os
import sys

import click
from rich import print as rprint

from common.output import write_output
from models.connection import parse_dsn
from repository.sqlalchemy_repo import SQLAlchemyRepository


@click.group()
@click.option(
    "--output",
    type=click.Choice(["console", "csv", "json", "parquet"]),
    default="console",
    help="Output format.",
)
@click.option(
    "--output-path",
    default=None,
    help="Output file path. Auto-generated if not specified.",
)
@click.pass_context
def cli(ctx: click.Context, output: str, output_path: str | None) -> None:
    """MainerSQL — RDBMS data extraction tool."""
    ctx.ensure_object(dict)
    ctx.obj["output"] = output
    ctx.obj["output_path"] = output_path


@cli.command()
@click.option("--query", required=True, help="SQL query to execute.")
@click.pass_context
def extract(ctx: click.Context, query: str) -> None:
    """Execute a SQL query and export the results."""
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        click.echo("Error: DATABASE_URL environment variable is not set.", err=True)
        sys.exit(1)

    config = parse_dsn(dsn)
    repo = SQLAlchemyRepository(config)
    table = repo.execute_query(query)

    output_format = ctx.obj["output"]
    output_path = ctx.obj["output_path"]
    result_path = write_output(table, output_format, output_path)

    if result_path is not None:
        rprint(f"[green]Output saved to: {result_path}")
