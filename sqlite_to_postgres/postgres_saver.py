import logging
import sqlite3
from typing import Generator, KeysView

import psycopg
from psycopg.errors import UndefinedTable

from sqlite_to_postgres.db_settings import COLUMN_MAPPING, FILTER_OUT_COLUMNS
from sqlite_to_postgres.models import T

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostgresSaver:
    def __init__(self, connection: psycopg.connection):
        self.connection = connection

    @staticmethod
    def _map_row(
            row: sqlite3.Row, column_mapping: dict, original_columns: KeysView
    ):
        return tuple(
            getattr(row, col) if col in column_mapping else getattr(row, col)
            for col in original_columns
            if col not in FILTER_OUT_COLUMNS
        )

    def load_data(
            self,
            transformed_data: Generator[list[T], None, None],
            table_name: str,
    ):
        pg_cursor = self.connection.cursor()
        try:
            for batch in transformed_data:
                original_columns = batch[0].__dict__.keys()
                mapped_columns = [
                    COLUMN_MAPPING.get(col, col)
                    for col in original_columns
                    if col not in FILTER_OUT_COLUMNS
                ]
                columns = ", ".join(mapped_columns)
                placeholders = ", ".join(["%s"] * len(mapped_columns))
                insert_query = (
                    f"INSERT INTO content.{table_name} ({columns}) "
                    f"VALUES ({placeholders}) "
                    f"ON CONFLICT (id) DO NOTHING"
                )
                pg_cursor.executemany(
                    insert_query,
                    [
                        self._map_row(row, COLUMN_MAPPING, original_columns)
                        for row in batch
                    ],
                )
                self.connection.commit()
        except UndefinedTable:
            logger.exception(f"The table '{table_name}' doesn't exist in the DB")
            self.connection.rollback()
        finally:
            pg_cursor.close()
