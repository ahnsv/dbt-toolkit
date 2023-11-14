from __future__ import annotations

import pytest

from dbttoolkit.core.io import read_sql_file
from dbttoolkit.core.sql import extract_table_references


@pytest.mark.parametrize(
    "sql_file,number_of_refs",
    [
        ("tests/data/complex-sample.sql", 4),
        ("tests/data/sample1.sql", 1),
    ],
)
def test_extract_table_references(sql_file, number_of_refs):
    sql = read_sql_file(sql_file)

    output = extract_table_references(sql_query=sql)

    assert output is not None
    assert len(output) == number_of_refs
