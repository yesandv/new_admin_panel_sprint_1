import sqlite3
from contextlib import contextmanager

import psycopg
from psycopg import ClientCursor
from psycopg.rows import dict_row

from sqlite_to_postgres.db_settings import TABLE_MAPPING, PG_DSL, SQLITE_DB_PATH
from sqlite_to_postgres.postgres_saver import PostgresSaver
from sqlite_to_postgres.sqlite_loader import SQLiteLoader


@contextmanager
def sqlite_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def postgres_connection(dsl: dict, **kwargs):
    conn = psycopg.connect(**dsl, **kwargs)
    try:
        yield conn
    finally:
        conn.close()


def run_etl():
    with sqlite_connection(SQLITE_DB_PATH) as sqlite_conn, postgres_connection(
            PG_DSL, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        sqlite_loader = SQLiteLoader(sqlite_conn)
        postgres_saver = PostgresSaver(pg_conn)

        for table_name, model in TABLE_MAPPING.items():
            data = sqlite_loader.extract_data(table_name)
            transformed_data = sqlite_loader.transform_data(data, model)
            postgres_saver.load_data(transformed_data, table_name)


if __name__ == "__main__":
    run_etl()
