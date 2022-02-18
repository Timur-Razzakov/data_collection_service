import os
import sys
import django

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")

django.setup()
# ---------------------------------------------------------------------------------

import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from schedule import every, repeat, run_pending

from scraping.models import Vacancies

"""
Функция для удаления старых записей
"""


class Command(BaseCommand):
    help = 'Delete objects older than 5 days'

    @repeat(every().sunday.at("15:25"))
    def handle(*args, **options):
        Vacancies.objects.filter(created_at__lte=datetime.now() - timedelta(days=5)).delete()
        # Vacancies.objects.filter(created_at__gte=datetime.now() - timedelta(days=5)).delete()


while 1:
    run_pending()
    time.sleep(1)
