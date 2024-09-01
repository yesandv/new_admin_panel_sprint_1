from dataclasses import dataclass, field
from datetime import date, datetime, UTC
from typing import TypeVar
from uuid import UUID


@dataclass
class Genre:
    id: UUID
    name: str
    description: str | None = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(UTC)
        if not self.updated_at:
            self.updated_at = datetime.now(UTC)


@dataclass
class GenreFilmWork:
    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created_at: datetime | None = field(default=None)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(UTC)


@dataclass
class PersonFilmWork:
    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created_at: datetime | None = field(default=None)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(UTC)


@dataclass
class Person:
    id: UUID
    full_name: str
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(UTC)
        if not self.updated_at:
            self.updated_at = datetime.now(UTC)


@dataclass
class FilmWork:
    id: UUID
    title: str
    type: str
    description: str | None = field(default=None)
    creation_date: date | None = field(default=None)
    file_path: str | None = field(default=None)
    rating: float | None = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(UTC)
        if not self.updated_at:
            self.updated_at = datetime.now(UTC)


T = TypeVar(
    "T", Genre, GenreFilmWork, PersonFilmWork, Person, PersonFilmWork, FilmWork
)
