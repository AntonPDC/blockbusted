#!/usr/bin/env python
"""Django's CLI entrypoint.

We default to the DEV settings module so `python manage.py runserver`
works out of the box after you create a `.env` file.
"""

import os
import sys

def main():
    # Default to dev settings for local development.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movielibrary.settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
