import os
from typing import Union

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account

from dbttoolkit.core.exceptions import dbtToolkitError


class TableNotFound(dbtToolkitError):
    pass


class ServiceAccountJSONNotFound(dbtToolkitError):
    pass


def create_client() -> bigquery.Client:
    try:
        credentials = service_account.Credentials.from_service_account_file(
            filename=os.getenv("CREDENTIAL_JSON_PATH", "service_account.json")
        )
    except FileNotFoundError:
        # click.exceptions.Exit(1)
        raise ServiceAccountJSONNotFound(
            name="Service Account JSON을 찾을 수 없습니다.\nCREDENTIAL_JSON_PATH 환경 변수를 세팅하거나, "
            "$PROJECT_ROOT/service_account.json 경로에 해당 파일을 추가해주세요"
        )
    bigquery_client = bigquery.Client(credentials=credentials)
    return bigquery_client


def get_bq_table(table_ref: Union[str, bigquery.TableReference], client: bigquery.Client = None) -> bigquery.Table:
    if not client:
        client = create_client()
    try:
        table_meta: bigquery.Table = client.get_table(table_ref)
    except NotFound:
        raise TableNotFound(name="테이블을 찾을 수 없습니다", details={"table_ref": table_ref})
    return table_meta


def check_if_table_exist(table_ref: Union[str, bigquery.TableReference], client: bigquery.Client = None) -> bool:
    if not client:
        client = create_client()
    table = get_bq_table(client=client, table_ref=table_ref)
    return table is not None
