import sqlite3

import psycopg
import pytest
from psycopg import ClientCursor
from psycopg.rows import dict_row

from sqlite_to_postgres.db_settings import PG_DSL, SQLITE_DB_PATH


@pytest.fixture
def sqlite_connection():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    yield conn
    conn.close()


@pytest.fixture
def pg_connection():
    conn = psycopg.connect(
        **PG_DSL, row_factory=dict_row, cursor_factory=ClientCursor
    )
    yield conn
    conn.close()
