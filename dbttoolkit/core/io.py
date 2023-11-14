from __future__ import annotations

from pathlib import Path


def read_sql_file(file: str | Path):
    if not file.endswith(".sql"):
        raise ValueError("Not sql file")
    with open(file) as f:
        input_data = f.read()
    return input_data
