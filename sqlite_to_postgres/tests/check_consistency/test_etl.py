from uuid import UUID

import pytest

from sqlite_to_postgres.db_settings import TABLE_MAPPING
from sqlite_to_postgres.models import (
    Genre,
    Person,
    FilmWork,
    GenreFilmWork,
    PersonFilmWork,
)
from sqlite_to_postgres.postgres_saver import PostgresSaver
from sqlite_to_postgres.sqlite_loader import SQLiteLoader


def _turn_uuid_into_str(row: dict) -> dict:
    return {
        key: (str(value) if isinstance(value, UUID) else value)
        for key, value in row.items()
    }


@pytest.mark.parametrize("table, model", list(TABLE_MAPPING.items()))
def test_data_count(sqlite_connection, pg_connection, table, model):
    sqlite_loader = SQLiteLoader(sqlite_connection)
    postgres_saver = PostgresSaver(pg_connection)

    extracted_data = sqlite_loader.extract_data(table)
    transformed_data = sqlite_loader.transform_data(extracted_data, model)
    postgres_saver.load_data(transformed_data, table)

    sqlite_cursor = sqlite_connection.cursor()
    pg_cursor = pg_connection.cursor()

    sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
    sqlite_count = sqlite_cursor.fetchone()[0]

    pg_cursor.execute(f"SELECT COUNT(*) FROM content.{table}")
    postgres_count = pg_cursor.fetchone()["count"]

    assert sqlite_count == postgres_count


def test_data_consistency_genre(sqlite_connection, pg_connection):
    table = "genre"
    columns = ", ".join(("id", "name", "description"))
    sqlite_loader = SQLiteLoader(sqlite_connection)
    postgres_saver = PostgresSaver(pg_connection)

    extracted_data = sqlite_loader.extract_data(table)
    transformed_data = sqlite_loader.transform_data(extracted_data, Genre)
    postgres_saver.load_data(transformed_data, table)

    sqlite_cursor = sqlite_connection.cursor()
    pg_cursor = pg_connection.cursor()

    sqlite_cursor.execute(f"SELECT {columns} FROM {table} ORDER BY id")
    sqlite_rows = [dict(**row) for row in sqlite_cursor.fetchall()]

    pg_cursor.execute(f"SELECT {columns} FROM content.{table} ORDER BY id")
    pg_rows = [_turn_uuid_into_str(row) for row in pg_cursor.fetchall()]

    assert sqlite_rows == pg_rows


def test_data_consistency_person(sqlite_connection, pg_connection):
    table = "person"
    columns = ", ".join(("id", "full_name"))
    sqlite_loader = SQLiteLoader(sqlite_connection)
    postgres_saver = PostgresSaver(pg_connection)

    extracted_data = sqlite_loader.extract_data(table)
    transformed_data = sqlite_loader.transform_data(extracted_data, Person)
    postgres_saver.load_data(transformed_data, table)

    sqlite_cursor = sqlite_connection.cursor()
    pg_cursor = pg_connection.cursor()

    sqlite_cursor.execute(f"SELECT {columns} FROM {table} ORDER BY id")
    sqlite_rows = [dict(**row) for row in sqlite_cursor.fetchall()]

    pg_cursor.execute(f"SELECT {columns} FROM content.{table} ORDER BY id")
    pg_rows = [_turn_uuid_into_str(row) for row in pg_cursor.fetchall()]

    assert sqlite_rows == pg_rows


def test_data_consistency_film_work(sqlite_connection, pg_connection):
    table = "film_work"
    columns = ", ".join(
        ("id", "title", "type", "description", "creation_date", "rating")
    )
    sqlite_loader = SQLiteLoader(sqlite_connection)
    postgres_saver = PostgresSaver(pg_connection)

    extracted_data = sqlite_loader.extract_data(table)
    transformed_data = sqlite_loader.transform_data(extracted_data, FilmWork)
    postgres_saver.load_data(transformed_data, table)

    sqlite_cursor = sqlite_connection.cursor()
    pg_cursor = pg_connection.cursor()

    sqlite_cursor.execute(f"SELECT {columns} FROM {table} ORDER BY id")
    sqlite_rows = [dict(**row) for row in sqlite_cursor.fetchall()]

    pg_cursor.execute(f"SELECT {columns} FROM content.{table} ORDER BY id")
    pg_rows = [_turn_uuid_into_str(row) for row in pg_cursor.fetchall()]

    assert sqlite_rows == pg_rows


def test_data_consistency_genre_film_work(sqlite_connection, pg_connection):
    table = "genre_film_work"
    columns = ", ".join(("id", "film_work_id", "genre_id"))
    sqlite_loader = SQLiteLoader(sqlite_connection)
    postgres_saver = PostgresSaver(pg_connection)

    extracted_data = sqlite_loader.extract_data(table)
    transformed_data = sqlite_loader.transform_data(
        extracted_data, GenreFilmWork
    )
    postgres_saver.load_data(transformed_data, table)

    sqlite_cursor = sqlite_connection.cursor()
    pg_cursor = pg_connection.cursor()

    sqlite_cursor.execute(f"SELECT {columns} FROM {table} ORDER BY id")
    sqlite_rows = [dict(**row) for row in sqlite_cursor.fetchall()]

    pg_cursor.execute(f"SELECT {columns} FROM content.{table} ORDER BY id")
    pg_rows = [_turn_uuid_into_str(row) for row in pg_cursor.fetchall()]

    assert sqlite_rows == pg_rows


def test_data_consistency_person_film_work(sqlite_connection, pg_connection):
    table = "person_film_work"
    columns = ", ".join(("id", "film_work_id", "person_id", "role"))
    sqlite_loader = SQLiteLoader(sqlite_connection)
    postgres_saver = PostgresSaver(pg_connection)

    extracted_data = sqlite_loader.extract_data(table)
    transformed_data = sqlite_loader.transform_data(
        extracted_data, PersonFilmWork
    )
    postgres_saver.load_data(transformed_data, table)

    sqlite_cursor = sqlite_connection.cursor()
    pg_cursor = pg_connection.cursor()

    sqlite_cursor.execute(f"SELECT {columns} FROM {table} ORDER BY id")
    sqlite_rows = [dict(**row) for row in sqlite_cursor.fetchall()]

    pg_cursor.execute(f"SELECT {columns} FROM content.{table} ORDER BY id")
    pg_rows = [_turn_uuid_into_str(row) for row in pg_cursor.fetchall()]

    assert sqlite_rows == pg_rows
