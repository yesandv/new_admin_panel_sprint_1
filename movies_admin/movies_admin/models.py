import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class FilmWorkType(models.TextChoices):
    MOVIE = ("movie", _("movie"))
    TV = ("tv_series", _("tv_series"))


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("genre_name"), max_length=300, unique=True)
    description = models.TextField(_("description"), null=True, blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=300)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.TextField(_("title"))
    description = models.TextField(_("description"), null=True, blank=True)
    creation_date = models.DateField(_("creation_date"), null=True, blank=True)
    rating = models.FloatField(
        _("rating"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    type = models.TextField(_("type"), choices=FilmWorkType.choices)
    genres = models.ManyToManyField(Genre, through="GenreFilmWork")
    people = models.ManyToManyField(Person, through="PersonFilmWork")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("film_work")
        verbose_name_plural = _("film_works")
        indexes = [
            models.Index(
                fields=["type", "rating"], name="film_work_type_rating_idx"
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "creation_date"],
                name="film_work_title_creation_date_idx",
            ),
        ]

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="genre_film_works"
    )
    film_work = models.ForeignKey(
        FilmWork, on_delete=models.CASCADE, related_name="genre_film_works"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        indexes = [
            models.Index(
                fields=["genre"], name="genre_film_work_genre_id_idx"
            ),
        ]


class PersonFilmWork(UUIDMixin):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="person_film_works"
    )
    film_work = models.ForeignKey(
        FilmWork, on_delete=models.CASCADE, related_name="person_film_works"
    )
    role = models.CharField(_("role"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        indexes = [
            models.Index(
                fields=["person"], name="person_film_work_person_id_idx"
            ),
        ]
