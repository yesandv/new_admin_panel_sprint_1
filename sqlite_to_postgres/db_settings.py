import os

from dotenv import load_dotenv

from sqlite_to_postgres.models import (
    Genre,
    GenreFilmWork,
    PersonFilmWork,
    Person,
    FilmWork,
)

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLITE_DB_PATH = BASE_DIR + os.getenv("SQLITE_DB")

PG_DSL = {
    "dbname": os.getenv("POSTGRES_NAME"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
    "port": os.getenv("POSTGRES_PORT", 5432),
}

BATCH_SIZE = 100

TABLE_MAPPING = {
    "genre": Genre,
    "person": Person,
    "film_work": FilmWork,
    "genre_film_work": GenreFilmWork,
    "person_film_work": PersonFilmWork,
}

COLUMN_MAPPING = {"created_at": "created", "updated_at": "modified"}

FILTER_OUT_COLUMNS = ["file_path"]
