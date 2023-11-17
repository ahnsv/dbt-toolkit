from __future__ import annotations

from pathlib import Path


def read_sql_file(file: str | Path):
    if not file.endswith(".sql"):
        raise ValueError("Not sql file")
    with open(file) as f:
        input_data = f.read()
    return input_data


def write_sql_file(file: str | Path, new_sql_content: str):
    with open(file, "w") as f:
        f.write(new_sql_content)
    return new_sql_content
