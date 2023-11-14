from __future__ import annotations

import inspect
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import typer

from dbttoolkit.core.io import read_sql_file
from dbttoolkit.core.sql import extract_table_references

app = typer.Typer()


@dataclass
class dbtSourceNode:
    name: str
    database: str
    schema: str
    identifier: str

    @classmethod
    def from_dict(cls, env):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


class dbtSourceNodeSet:
    def __init__(self, nodes: dict[str, Any], project_name: str):
        self.nodes = nodes
        self.project_name = project_name

    def search_by_schema_and_table_name(self, schema: str, table_name: str):
        value: dict[str, Any] | None = self.nodes.get(f"source.{self.project_name}.{schema}.{table_name}")
        if not value:
            return
        return dbtSourceNode.from_dict(value)


@app.command(help="convert a plain sql to dbt jinja sql, replacing existing source node with dbt expression")
def convert_to_dbt_jinja(sql_file_path: str, dbt_project_path: Path):
    sql = read_sql_file(sql_file_path)
    table_refs = extract_table_references(sql_query=sql)

    manifest_json_path = dbt_project_path / "target/manifest.json"
    if not manifest_json_path.exists():
        raise FileNotFoundError(f"{manifest_json_path}")
    with open(manifest_json_path) as f:
        manifest_json = json.load(f)

    source_node_set = dbtSourceNodeSet(
        manifest_json["sources"], project_name=manifest_json["metadata"]["project_name"]
    )
    for table_ref in table_refs:
        project, dataset, table = table_ref.value.replace("`", "").split(".")
        source_node = source_node_set.search_by_schema_and_table_name(schema=dataset, table_name=table)
        if not source_node:
            should_add = typer.confirm(f"[Add] {table_ref.value} is not existing in manifest.json. Should we add it?")
            if should_add:
                # TODO: add
                ...
            continue
        should_replace = typer.confirm(
            f"[Replace] {table_ref.value} ➡️ {{{{ source('{source_node.schema}', '{source_node.identifier}') }}}}. Is it OK?"
        )
        if should_replace:
            sql = sql.replace(
                table_ref.value,
                f"{{{{ source('{source_node.schema}', '{source_node.identifier}') }}}}",
            )

    print(sql)


@app.command(
    help="find your source, scan it from your connection, and sync columns, description, etc. to your sources.yaml"
)
def update_source_from_dw(source_ref: str):
    raise NotImplementedError


@app.command(help="read your sql file, extract CTE statement and make dbt models out of them")
def extract_cte_to_model(sql_file: Path, model_name: str, should_replace: bool):
    raise NotImplementedError


if __name__ == "__main__":
    app()
