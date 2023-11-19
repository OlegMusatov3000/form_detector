from django.core.management.base import BaseCommand

from form_detector_backend.settings import ALL_TEMPLATES
from ...models import FormTemplate


class Command(BaseCommand):
    help = 'Команда выполняет загрузку шаблонов в базу данных TinyDB.'

    def handle(self, *args, **kwargs):
        for name, fields in ALL_TEMPLATES:
            FormTemplate(name=name, fields=fields).save()
