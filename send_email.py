import datetime
import os
import sys
import django
from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
django.setup()
# -------------------------------------------------------------------------------

from django.core.mail import EmailMultiAlternatives
from scraping.models import Vacancies
from icecream import ic
from service.settings import (
    EMAIL_HOST_USER,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD
)

today = datetime.date.today()
subject = f"Рассылка вакансий за {today}"
text_content = f"Рассылка вакансий {today}"
ADMIN_USER = EMAIL_HOST_USER
empty = '<h2> Нет результат по вашему запросу </h2>'

User = get_user_model()

qs = User.objects.filter(send_email=True).values('city', 'speciality', 'email')
user_dct = {}
for item in qs:
    user_dct.setdefault((item['city'], item['speciality']), [])  # 3параметр, это тип (список)
    user_dct[(item['city'], item['speciality'])].append(item['email'])

if user_dct:
    # поиск всех значений, которые принадлежат данной паре
    params = {'city_id__in': [], 'speciality_id__in': []}

    for pair in user_dct.keys():
        params['city_id__in'].append(pair[0])
        params['speciality_id__in'].append(pair[1])
    qs = Vacancies.objects.filter(**params).values()[:10]
    vacancy = {}
    for item in qs:
        vacancy.setdefault((item['city_id'], item['speciality_id']), [])
        vacancy[(item['city_id'], item['speciality_id'])].append(item)
    for keys, emails in user_dct.items():
        rows = vacancy.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
            html += f'<p><strong>{row["salary"]}</strong></p>'
            html += f'<p><strong>{row["company_name"]}</strong></p>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(
                subject, text_content, ADMIN_USER, [to]
            )
            msg.attach_alternative(_html, "text/html")
            msg.send()