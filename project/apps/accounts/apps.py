"""Accounts app config.

`label = "accounts"` ensures the database table names and app label
are stable and short.
"""

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
