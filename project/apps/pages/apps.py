"""Pages app.

This is intentionally tiny:
- gives you `/` that loads your CSS, proving static wiring works
- you can remove this app later if you only want API-only backend
"""

from django.apps import AppConfig

class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pages"
    label = "pages"
