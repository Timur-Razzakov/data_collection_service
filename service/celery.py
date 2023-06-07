
import os

import django
from celery import Celery
from celery.schedules import crontab

# Установили переменную окружения с именем вашего проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')
django.setup()
# ---------------------------------------------------------------------------------
# Создайте экземпляр Celery для нашего проекта
app = Celery('service')

# Загрузите конфигурацию из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

CELERY_BEAT_SCHEDULE = {
    'run-every-day-at-5': {
        'task': 'reminder.tasks.run_scripts_task',
        'schedule': crontab(hour=19, minute=53),
    },

    'run-every-day-at-7': {
        'task': 'reminder.tasks.send_email_task',
        'schedule': crontab(hour=6, minute=30),
    },
    'run-every-week-at-9': {
        'task': 'reminder.tasks.delete_old_task',
        'schedule': crontab(day_of_week=1, hour=11, minute=0),
    },
}
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE
app.conf.timezone = 'Asia/Tashkent'
# Загрузите задачи из всех файлов tasks.py в приложениях Django
app.autodiscover_tasks()

# Импортируйте вашу таску здесь