from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoviesAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "movies_admin"
    verbose_name = _("movies_admin")
