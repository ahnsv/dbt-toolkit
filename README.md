# dbt Toolkit
Swiss knife for everyday dbt works

[![PyPI version](https://badge.fury.io/py/dbt-tool-kit.svg)](https://badge.fury.io/py/dbt-tool-kit)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbt-tool-kit)

![GitHub Repo stars](https://img.shields.io/github/stars/ahnsv/dbt-toolkit)

## Installation
```shell
pip install dbt-tool-kit
```

## Usage
```shell
> dbt-toolkit --help

 Usage: dbt-toolkit [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                             │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                      │
│ --help                        Show this message and exit.                                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ convert-to-dbt-jinja          convert a plain sql to dbt jinja sql, replacing existing source node with dbt expression                                              │
│ extract-cte-to-model          read your sql file, extract CTE statement and make dbt models out of them                                                             │
│ update-source-from-dw         find your source, scan it from your connection, and sync columns, description, etc. to your sources.yaml                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
