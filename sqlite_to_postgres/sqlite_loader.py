import logging
import sqlite3
from typing import Generator

from sqlite_to_postgres.db_settings import BATCH_SIZE
from sqlite_to_postgres.models import T

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def extract_data(
            self, table_name: str
    ) -> Generator[list[sqlite3.Row], None, None]:
        sqlite_cursor = self.connection.cursor()
        try:
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        except sqlite3.OperationalError:
            logger.exception(f"No such table '{table_name}' in the DB")
        while rows := sqlite_cursor.fetchmany(BATCH_SIZE):
            yield rows

    @staticmethod
    def transform_data(
            rows: Generator[list[sqlite3.Row], None, None], model: type[T]
    ) -> Generator[list[T], None, None]:
        for batch in rows:
            yield [model(**dict(row)) for row in batch]
