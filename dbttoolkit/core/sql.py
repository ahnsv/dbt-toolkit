from __future__ import annotations

import logging
import os
import re
import sys

import sqlparse

from dbttoolkit.dialect.bigquery import check_if_table_exist

IS_DEBUG = os.getenv("ENV", "dev") == "dev"
logging.basicConfig(
    level=logging.DEBUG if IS_DEBUG else logging.ERROR,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s - %(message)s",
)
logger = logging.getLogger("source_transform")


class SourceTransformFileNotFoundError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def read_sql_file(sql_file_path: str) -> str:
    try:
        with open(sql_file_path) as f:
            sql = f.read()
    except FileNotFoundError:
        raise SourceTransformFileNotFoundError(message=f"파일을 찾을 수 없습니다\t[input file path: {sql_file_path}]", code=404)

    return sql


def find_table_full_ref(sql: str) -> tuple[str, set[str]]:
    pattern = r"`.*\..*\..*`"
    source_list = re.findall(pattern, sql)
    logger.debug(source_list)
    source_set_ = set(source_list)

    return sql, source_set_


def _model_exists(model_layer_path: str, model_name: str) -> bool:
    return os.path.isfile(os.path.join(model_layer_path, f"{model_name}.sql"))


def get_source_jinja(
    project_id: str, dataset_id: str, table_id: str
) -> str | None:  # TODO : 디렉토리가 변경되어도 적용될 수 있도록 수정한다.
    # check if model exists in the project
    # if _model_exists(MART_DIR, table_id):
    #     return f"{{{{ ref('{table_id}') }}}}"
    #
    # if _model_exists(ODS_DIR, f"ods_{table_id}"):
    #     return f"{{{{ ref('ods_{table_id}') }}}}"

    if not check_if_table_exist(f"{project_id}.{dataset_id}.{table_id}"):
        return

    return f"{{{{ source('{dataset_id}', '{table_id}') }}}}"


def replace_table_full_ref_to_source_jinja(sql: str, source_set_: set[str]) -> str:
    copy = sql
    for source_table_full_ref in source_set_:
        [project_id, dataset_id, table_id] = source_table_full_ref.strip("`").split(".")
        if "udf" not in dataset_id:
            source_jinja = get_source_jinja(project_id, dataset_id, table_id)
            copy = copy.replace(source_table_full_ref, source_jinja)
    logger.debug(copy)
    return copy


def source_transform(query_path: str) -> str:
    sql_in_str = read_sql_file(query_path)
    sql_in_str, source_set = find_table_full_ref(sql_in_str)
    return replace_table_full_ref_to_source_jinja(sql_in_str, source_set)


def write_transformed_result(result, sql_file_path):
    with open(sql_file_path, "w") as f:
        f.write(result)


def match_table_reference(table_ref_like: str):
    pattern = re.compile(r"^(`?\[?[a-zA-Z0-9_\-]+\]?`?\.)+(`?\[?[a-zA-Z0-9_\-]+\]?`?)$")
    return bool(pattern.match(table_ref_like))


def extract_table_references(sql_query: str):
    parsed = sqlparse.parse(sql_query)
    table_references = []

    def recurse_statement(statement_: sqlparse.sql.Statement):
        if not hasattr(statement_, "tokens"):
            if statement_.ttype == sqlparse.tokens.Name:
                table_references.append(statement_)
            return

        if statement_.is_group and statement_.ttype is None:
            names = [
                token
                for token in statement_.tokens
                if token.ttype == sqlparse.tokens.Name and match_table_reference(table_ref_like=token.value)
            ]
            for name in names:
                table_references.append(name)

        for item in statement_.tokens:
            if (
                isinstance(item, sqlparse.sql.Identifier)
                or isinstance(item, sqlparse.sql.Parenthesis)
                or isinstance(item, sqlparse.sql.IdentifierList)
            ):
                recurse_statement(item)

    for statement in parsed:
        recurse_statement(statement)

    return table_references
