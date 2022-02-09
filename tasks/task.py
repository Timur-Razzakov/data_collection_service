# import os
# import sys
# import django
#
# #  you have to set the correct path to you settings module
# from icecream import ic
#
# proj = os.path.dirname(os.path.abspath('manage.py'))
# sys.path.append(proj)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
# django.setup()
# # -----------------------------------------------------------------------------
# from service.celery import app
# from django.core.management.base import BaseCommand
# from scraping.models import Vacancies
# from datetime import datetime, timedelta
#
# """
# Функция для удаления старых записей
# """
#
#
# @app.task
# class Command(BaseCommand):
#     help = 'Delete objects older than 5 days'
#
#     def handle(self, *args, **options):
#         vacancy = Vacancies.objects.filter(created_at__lte=datetime.now() - timedelta(days=5))
#         vacancy.delete()
#         self.stdout.write('Deleted objects older than 5 days')
#
#
# Command.delay()
