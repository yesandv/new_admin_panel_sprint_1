from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    search_fields = ("title", "type", "rating")
    list_display = ("title", "type", "description", "rating")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    _fields = ("name", "description")
    search_fields = _fields
    list_display = _fields


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)
