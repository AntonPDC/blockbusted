#!/usr/bin/env python
"""Django management entrypoint.

This is what runs when you execute:
- `python manage.py runserver`
- `python manage.py migrate`
- etc.

We set DJANGO_SETTINGS_MODULE to our single settings file.
"""

import os
import sys

def main():
    # Points Django at blockbusted/settings.py
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blockbusted.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
