from dataclasses import dataclass
from typing import Literal


@dataclass
class ConnectionConfig:
    dsn: str
    dialect: Literal["postgresql", "mssql"]


def parse_dsn(url: str) -> ConnectionConfig:
    """Detect dialect from DSN URL prefix."""
    url_lower = url.lower()
    if url_lower.startswith("postgresql") or url_lower.startswith("postgres"):
        return ConnectionConfig(dsn=url, dialect="postgresql")
    elif url_lower.startswith("mssql"):
        return ConnectionConfig(dsn=url, dialect="mssql")
    raise ValueError(f"Unsupported DSN dialect: {url!r}")
