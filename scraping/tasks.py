
from service.celery import app
from django.core.management.base import BaseCommand
from scraping.models import Vacancies
from datetime import datetime, timedelta

"""
Функция для удаления старых записей
"""


@app.task
class Command(BaseCommand):
    help = 'Delete objects older than 5 days'

    def handle(self, *args, **options):
        vacancy = Vacancies.objects.filter(created_at__lte=datetime.now() - timedelta(days=5))
        vacancy.delete()
        self.stdout.write('Deleted objects older than 5 days')


Command.delay()
