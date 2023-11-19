"""
Custom Django management command for loading templates into the TinyDB
database.

This command loads templates from the ALL_TEMPLATES list defined in the
settings module and saves them to the TinyDB database using the FormTemplate
model.

Dependencies:
- Django: A high-level Python web framework.
- TinyDB: A lightweight database for Python.

Usage:
python manage.py load_db
"""

from django.core.management.base import BaseCommand

from form_detector_backend.settings import ALL_TEMPLATES
from ...models import FormTemplate


class Command(BaseCommand):
    help = 'Команда выполняет загрузку шаблонов в базу данных TinyDB.'

    def handle(self, *args, **kwargs):
        """
        Iterates through the ALL_TEMPLATES list and saves each template to the
        TinyDB database.
        """
        for name, fields in ALL_TEMPLATES:
            FormTemplate(name=name, fields=fields).save()
        print("✅ Data saved successfully!")
