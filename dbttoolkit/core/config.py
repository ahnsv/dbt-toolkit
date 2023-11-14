from dataclasses import dataclass


@dataclass
class dbtToolkitConfig:
    connection: str
    dbt_model_path: str
